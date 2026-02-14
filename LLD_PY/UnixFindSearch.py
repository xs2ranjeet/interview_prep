'''
Unix file command searches for files. Now there can be different search criteria's like search by file size, or 
search by extension or by a substring in file name. e.g. list all files which are less than 2 MB size or list all 
files whose extension is .pdf.
You can use strategy design pattern to implement the different search criteria's.
A follow up is generally asked to combine queries like Boolean predicates AND, OR etc. e.g. list all files which are 
greater than 2MB in size AND their extension is “.jpg”.
You can use specification design pattern to combine result of search queries.
Design an in-memory file lookup tool similar to the Unix find command that:
Supports multiple search criteria:
File size
File extension
File name substring (easily extensible)
Supports Boolean composition of queries:
AND
OR
NOT
'''
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

# make file immutable best practice
# @dataclass(frozen=True) 
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.extension = name.split(".")[-1] if "." in name else ""

    def __repr__(self):
        return f"File({self.name},{self.size})"
    
class SearchStrategy(ABC):

    @abstractmethod
    def match(self, file: File):
        pass

class Specification(ABC):

    @abstractmethod
    def isSatisfied(self, file: File) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)
    
    def __or__(self, other):
        return OrSpecification(self, other)
    
    def __invert__(self):
        return NotSpecification(self)
    
class SizeGreaterThanSearchCriteria(SearchStrategy):
    def __init__(self, size):
        self.size = size

    def match(self, file):
        return file.size > self.size
    
class SizeSmallerThanSearchCriteria(SearchStrategy):
    def __init__(self, size):
        self.size = size

    def match(self, file):
        return file.size < self.size
    
class ExtensionSearchCriteria(SearchStrategy):
    def __init__(self, extension):
        self.extension = extension

    def match(self, file):
        return file.extension == self.extension
    
class AnyExtensionSearchCriteria:
    def __init__(self, extensions: List[str]):
        self.extensions = set(extensions)

    def match(self, file):
        return file.extension in self.extensions
    
class NameSearchCriteria:
    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, file):
        return self.pattern in file.name 

class AndSpecification(Specification):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def isSatisfied(self, file):
        return self.left.isSatisfied(file) and self.right.isSatisfied(file)
    
class OrSpecification(Specification):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def isSatisfied(self, file):
        return self.left.isSatisfied(file) or self.right.isSatisfied(file)
    
class NotSpecification(Specification):
    def __init__(self, left):
        self.left = left

    def isSatisfied(self, file):
        return not self.left.isSatisfied(file) 
    
class SizeGreaterThanSpec(Specification):
    def __init__(self, size):
        self.size = size

    def isSatisfied(self, file):
        return file.size > self.size

class ExtensionSpec(Specification):
    def __init__(self, ext):
        self.ext = ext.split(".")[-1] if "." in ext else ext

    def isSatisfied(self, file):
        return file.extension == self.ext
    
class NameContainSpec(Specification):
    def __init__(self, substring):
        self.substring = substring

    def isSatisfied(self, file):
        return self.substring in file.name    


class SpecificationFileSearcher:
    def __init__(self):
        pass

    def search(self, files: List[File], spec: Specification):
        result = []
        for file in files:
            if spec.isSatisfied(file):
                result.append(file)
        return result

class FileSearcher:
    def __init__(self):
        pass
    def search(self, files: List[File], criteria: SearchStrategy):
        result = []
        for file in files:
            if criteria.match(file):
                result.append(file)
        return result


def driverCode():
    files = [File("Photo.jpg", 5000000), File("resume.pdf", 200000), File("movie.mp4", 9000000000), File("pic.jpg", 1000000), File("notes.txt", 50000)]

    searcher = FileSearcher()
    smallFile = SizeSmallerThanSearchCriteria(2000000)
    smallResult = searcher.search(files, smallFile)
    print(smallResult)
    
    # -------- Specification Pattern Example ----------
    specFS = SpecificationFileSearcher()
    jpegSpec = ExtensionSpec(".jpg")
    sizeSpec = SizeGreaterThanSpec(20000)
    ## (size > 2MB) AND (extension == .jpg)
    combined = sizeSpec and jpegSpec
    result = specFS.search(files, combined)
    print(result)

driverCode()