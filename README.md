SwiftFormat
==============

Python script for auto formatting Swift code, similar to Clang format.
 
 Current status: Gonna rewrite this to Swift.

## Usage

#### auto format a file
```bash
Usage: 
--file [FILE] The file to format
--output [FILE] The file to write the formatted output to

python format.py --file inputfilename.swift --output outputfilename.swift
```
### Demo

![Demo script run](https://raw.githubusercontent.com/haaakon/SwiftFormat/b746a3d8e7e067faecc8997fc4b9acd17b5ecb5f/swiftformat.gif)

### Contributing

All contributions are more than welcome, suggestions on how to move forward is appreciated.

### Test format
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

For each rule thats added, add a test file that shows how it should format correctly. The test checks that all files are formatted correctly as shown under the @@@ in their file.

#### Run tests
```bash
python tests.py
TEST OK for python/SwiftFormatter/testCases/indentation/indentTest.test
TEST OK for python/SwiftFormatter/testCases/indentation/lotsOfCurlyBraces.test
TEST OK for python/SwiftFormatter/testCases/indentation/mulitplemethodsinclass.test
TEST OK for python/SwiftFormatter/testCases/indentation/prefixedSpaces.test
TEST OK for python/SwiftFormatter/testCases/indentation/twoCurly.test
```



### TODO
- Add alot more formatting rules
- be able to turn rules on/off
- add a plugin for xcode

## License
MIT
### Author 
Håkon Bogen hakon.bogen@gmail.com
