# Subparse - Python



## Development
---


Below is examples of develping the Vue side for both parsers and enrichers. These can be used as 'templates' to develop your own custom Vue for the corresponding module.

### General Requirements
---
There are some basic requirements that all of the parser/enrichers will need to follow to allow them to be used by the program.

<details>
<summary>Filename</summary>
</br>
Regardless, if you are making an enricher or a parser the general filename will be the same, but there is a bit of a case different. Please make sure that the filename is correct for the type of module that is being created.

* TESTParser.py
* testenricher.py

</details>

<details>
<summary>Class Name</summary>
</br>
In the export default section of your vue page, there is parameter called name. This parameter needs to match the filename of the page. Below are two examples that match the filename examples shown above.

* TESTParser
* TESTEnricher

</details>
<p>&nbsp;</p>
</br>

### Parser Example
---


Below is a template for developing the Python file that is needed when developing a custom parser module.

General file information: 
* Location to place the .py file within the framework: subparse/parser/src/parsers/
* File naming schema: [parser name]Parser.py

There are a few things that you need to change when implementing your version of the template:

| Location | Change | Reason |
| ----------- | ----------- | ----------- |
| TESTParser | [Your Parser]Parser | The class name should match the name of the file excluding the extension. ALL instances of the ALTParser within the template should be replaced with [Your Parser]Parser |
| "short_type" : "pe" | "short_type" : "[File Type]" | The file type should not be the extension but the file type from file magic. For instance if the parser is for PDF files you should change the short_type value to be "pdf" |
| "other_types" : ["pe32"] | "other_types" : ["Other", "potential", "types"] | This needs to be changed to either being an empty array or an array where the indexs are strings with other potential types. For example if a compression parser other potential types might be, "zip", "rar", "rar5", etc. |

Note: All data that needs to be available or collected from the parser MUST be included into the self.data dictionary which is then returned to our framework to then be saved to the Elasticsearch cluster.

</br>
<details>
<summary>Parser Template Example</summary>
</br>

```python
import os
from typing import Any
from src.helpers import Command

class TESTParser(Command):
    """
    [Your Parser] - [Description about it]
    """
    def __init__(self, name: str = None, path: os.path = None) -> None:
        super().__init__()
        self.name = name
        self.path = path
        self.data = {}
        
    def information(self):
        return {"name": "ALTParser", "file_magic" : {"short_type" : "pe", "other_types" : ["pe32"]}}

    # region Execute ( For Command Object )
    def execute(self) -> Any:
        """
        Collects PE Information and is executed by the command invoker
        """
        # Custom Code Goes Here
        
        return {"parser" : "TESTParser", "data" : self.data}
    # endregion

```
</details>
<p>&nbsp;</p>


### Enricher Example
---


Below is a template for developing the Python file that is needed when building out a custom enricher module.

General file information: 
* Location to place the Vue.js file within the framework: subparse/parser/src/enrichers/
* File naming schema: [parser name]enricher.py

Note: Filename should be ALL lowercase


| Location | Change | Reason |
| ----------- | ----------- | ----------- |
| TESTEnricher | [Your Enricher]Enricher | The naming schema of the class should match the file but with a different casing. Your enricher name should be in all caps followed by Enricher. All instances of ABUSEEnricher need to be replaced with [Your Enricher]Enricher | 

Note: All data that needs to be available or collected from the parser MUST be included into the self.data dictionary which is then returned to our framework to then be saved to the Elasticsearch cluster.


</br>
<details>
<summary>Enricher Template Example</summary>
</br>

```python
from logging import Logger
import requests
from src.helpers import Command

class TESTEnricher(Command):
    """
    [Your Enricher] - [Description about it]
    """
    def __init__(self, md5: str, logger: Logger, path: str):
        super().__init__()
        self.md5 = md5
        self.logger = logger
        self.path = path
        self.data = {}
        

    def information(self):
        return {"name": "TESTEnricher"}

    def execute(self) -> dict:
        """
        Requests information about the malwares hash and returns the json request back to the invoker
        """

        return {"enricher": "TestEnricher", "data": self.data}

```
</details>
<p>&nbsp;</p>
