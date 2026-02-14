## Salesforce

'''
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
'''

from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Set
from threading import RLock
import hashlib

class User:
    def __init__(self, country: str = "", tier: str = ""):
        self.id = str(uuid4())
        self.country = country
        self.tier = tier

class Rule(ABC):

    @abstractmethod
    def match(self, user: User):
        pass

class CountryRule(Rule):
    def __init__(self, country: str, enabled: bool):
        self.country = country
        self.enabled = enabled

    def match(self, user: User):
        return self.country == user.country and self.enabled
    
class TierInRule(Rule):
    def __init__(self, tiers: List[str]):
        self.tiers = tiers

    def match(self, user: User):
        return user.tier in self.tiers
    

class FeatureFlag:
    def __init__(self, key: str,enabled: bool = False, rollout: float = 100):
        self.key = key
        self.enabled = False
        self.rollout = 0.0
        self.rules: List[Rule] = []

    def addRule(self, rule: Rule):
        self.rules.append(rule)

    def enableRollout(self, percent: float):
        self.rollout = percent

    def set_enabled(self, enabled: bool):
        self.enabled = enabled



class Rollout:
    @staticmethod
    def isFeatureEnabled(user_id: str, flag_key: str, percentage: float):
        if percentage <= 0:
            return True
        if percentage >= 100:
            return True
        
        key = f"{user_id}:{flag_key}".encode()
        hash_val = int(hashlib.sha256(key).hexdigest(), 16)
        bucket = hash_val % 100
        return bucket < percentage


class FeatureFlagEngine:
    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.lock = RLock()     

    def refresh_flags(self, flags: Dict[str, FeatureFlag],
                      dependencies: Dict[str, List[str]]):
        with self.lock:
            self.flags = flags
            self.dependencies = dependencies


    def isFeatureEnabled(self, user: User, flag_key: str) -> bool:
        with self.lock:
            return self._evaluate_flag(user, flag_key, set(), {})
        
    def _evaluate_flag(self, user: User, flag_key: str, visiting: Set[str], memo: dict) -> bool:
        if flag_key in memo:
            return memo[flag_key]
        if flag_key not in self.flags:
            memo[flag_key] = False
            return False
        if flag_key in visiting:
            memo[flag_key] = False
            return False
        visiting.add(flag_key)
        flag = self.flags[flag_key]

        try:
            for dep in self.dependencies.get(flag_key, {}):
                if not self._evaluate_flag(user, dep, visiting, memo):
                    memo[flag_key] = False
                    return False
            if flag.rules:
                eligible = any(rule.matches(user) for rule in flag.rules)
                if not eligible:
                    memo[flag_key] = False
                    return False
                
            if flag.rollout > 0:
                result = Rollout.isFeatureEnabled(user.id, flag_key, flag.rollout)
                memo[flag_key] = True
                return True
            
            memo[flag_key] = flag.enabled
            return flag.enabled
        finally:
            visiting.remove(flag_key)

# flag = FeatureFlag("new_ui")
# flag.rollout = 70
# flag.rules.append(CountryRule("EU", True))
# flag.rules.append(TierInRule(["Premium"]))

engine = FeatureFlagEngine()

# Flags
beta = FeatureFlag("beta_access")
beta.set_enabled(True)
beta.rollout = 70

new_ui = FeatureFlag("new_ui", enabled = True, rollout = 70)
checkout = FeatureFlag("checkout_redesign",  enabled = True, rollout = 70)

flags = {
    "beta_access": beta,
    "new_ui": new_ui,
    "checkout_redesign": checkout
}

dependencies = {
    "new_ui": ["beta_access"],
    "checkout_redesign": ["new_ui"]
}

engine.refresh_flags(flags, dependencies)

user = User(country="EU", tier="Free")

print(engine.isFeatureEnabled(user, "checkout_redesign"))
