/*
We need to build an in-house Feature Flag & Experiment Engine (local evaluator) that client applications (web/mobile/backend) will embed.

The evaluator must support:
1. Feature Flag Types
    Boolean flag (ON/OFF)
    Percentage rollout flag (e.g., show to 20% of users)
    Targeting rules, e.g.:
        user.country == "EU"
        user.tier IN ["Premium", "Enterprise"]
2. API
    bool isFeatureEnabled(const User& user, const std::string& flagKey);

3. How evaluation works
    If flagKey does not exist → return default (false)
    Apply targeting rules
    If user matches rule → return the rule's “result”
    Otherwise apply percentage rollout
    Otherwise return default value

4. Requirements
- In-memory data model
- No network calls
- Thread-safe reads
- Flags can be updated at runtime (e.g., through a refresh method)


-----------
Flags may depend on other flags.

Example:
"new_ui" depends on "beta_access"
"checkout_redesign" depends on "new_ui"


A flag is enabled only if all its dependencies are enabled.

Input- 
dependencies = [
  ["new_ui", "beta_access"],
  ["checkout_redesign", "new_ui"],
  ["discount_banner", "experiment_group"]
]


enabled = ["beta_access", "experiment_group"]
flagToEvaluate = "checkout_redesign"


Output- 
false
*/
#include <bits/stdc++.h>
using namespace std;

struct User {
    string id;
    string country;
    string tier;
};

class Rule {
    virtual ~Rule() = default;
    virtual bool evaluate(const User& user) const = 0;
};

class CountryRule: public Rule {
    string targetCountry;
    // const
    
    bool evaluate(const User& user) override {
        return user.country == targetCountry;
    }
};

class TierRule: public Rule {
    std::unordered_set<string> allowedTiers;

    TierRule(vector<string> tiers) {
        for(auto tier: tiers)
            allowedTies.insert(tier);
    }
    bool evaluate(const User& user) override {
        return allowedTiers.count(user.tier) > 0;
    }
};

struct FeatureFlag {
    string flagkey;
    bool defaultValue;
    vector<shared_ptr<Rule>> rules;
    bool ruleResult;
    int percentageRollout;
    vector<string> dependencies;
};

class FeatureFlagEvalutator {
    unordered_map<string, FeatureFlag> flags;
    mutable shared_mutex mutex;

    int hashUser(const string& userid) const {
        std::hash<string> hasher;
        return hasher(userid) % 100;
    }


    // Check if all dependencies are enabled (DFS with cycle detection)
    bool areDependenciesEnabled(const User& user, const std::string& flagKey, std::unordered_set<std::string>& visiting, std::unordered_set<std::string>& visited) const {
            if(visiting.count(flagKey))
                return false; // cycle detected
            if(visited.count(flagKey))
                return true; // already computed
            std::shared_lock lock(mutex);
            if(flags.count(flagKey) == 0)
                return false;
            auto flag = flags[flagKey];
            visiting.insert(flagKey);

            for(auto &dep: flag.dependencies) {
                if(!areDependenciesEnabled(user, dep, visiting, visited)) {
                    visiting.erase(flagKey);
                    return false;
                }
            }
            visiting.erase(flagKey);
            visited.insert(flagKey);    
                
            return evaluateFlagWithoutDep(user, flag);
    }

    bool evaluateFlagWithoutDep(const User& user, FeatureFlag& flag) {
        for(auto rule: flags.rules) {
            if(rule.evalute(user))
                return flag.ruleResult;
        }

        if(flag.percentileRollout > 0) {
            int userHash = hasher(user.id);
            if(userHash < flag.percentileRollout)
                return true;
        }
        return flag.defaultvalue;
    }

    // public
    void addFlag(string key, FeatureFlag flag) {
        unique_lock lock(mutex);
        flags[key] = flag;
    }

    bool isFeatureEnabled(const User& user, const std::string& flagkey) const {
        unordered_set<string> visiting;
        unordered_set<string> visited;
        return areDependenciesEnabled(user, flagKey, visiting, visited);
    }
};
