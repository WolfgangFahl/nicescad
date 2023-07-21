'''
Created on 2023-06-19

@author: wf
'''
import nicescad
class Version(object):
    """
    Version handling for nicescad
    """
    name = "nicescad"
    version = nicescad.__version__
    date = '2023-07-19'
    updated = '2023-07-21'
    description = 'Nice Scad',
    
    authors = 'Wolfgang Fahl'
    
    doc_url="https://wiki.bitplan.com/index.php/nicescad"
    chat_url="https://github.com/WolfgangFahl/nicescad/discussions"
    cm_url="https://github.com/WolfgangFahl/nicescad"

    license = f'''Copyright 2023 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.'''
    longDescription = f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""