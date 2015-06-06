SwiftFormat
==============

Python script for auto formatting Swift code, similar to Clang format.
 

## Usage

#### auto format a file
```bash
Usage: 
--file [FILE] The file to format
--output [FILE] The file to write the formatted output to

python format.py --file inputfilename.swift --output outputfilename.swift
```

### Tests
For each rule thats added, add a test file that shows how it should format correctly.

####Run tests
```bash
python tests.py
TEST OK for python/SwiftFormatter/testCases/indentation/indentTest.test
TEST OK for python/SwiftFormatter/testCases/indentation/lotsOfCurlyBraces.test
TEST OK for python/SwiftFormatter/testCases/indentation/mulitplemethodsinclass.test
TEST OK for python/SwiftFormatter/testCases/indentation/prefixedSpaces.test
TEST OK for python/SwiftFormatter/testCases/indentation/twoCurly.test
```
####Test format
Put source code to be formatted above @@@, and under put the correct way it should be formatted after running the format script.

```swift
class test() {{var str = "teststr" }}
@@@
class test() {
    {
        var str = "teststr"
    }
}
```

### TODO
- Add alot more formatting rules
- be able to turn rules on/off
- add a plugin for xcode

## License
MIT
### Author 
Håkon Bogen hakon.bogen@gmail.com
