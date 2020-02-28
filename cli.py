import os
import sys
from pprint import pprint
import templates
 

class Template:
    def __init__(self, action_name, stateful=False, *args, **kwargs):
        self.stateful = stateful
        self.action_name = action_name
        self.const = None
        self.types = None
        self.interfaces = None
        self.namespaces = {
            'camel_case': self._camel_case(),
            'snake_case': self._snake_case()
        }

    def connect_actiontypes(self, filename):
        print(filename)

    def _camel_case(self):
        if self.stateful:
            begin = self.action_name+"Begin"
            success = self.action_name+"Success"
            error = self.action_name+"Error"
            return [begin, success, error]
        else:
            return [self.action_name]

    def _snake_case(self):

        indexes = []
        [indexes.append(counter) for counter, element in enumerate(
            list(self.action_name)) if element.isupper()]

        last_index = 0
        text = ""

        last_index = 0
        text = ""

        for counter, item in enumerate(list(self.action_name)):
            if counter == 0:
                text += item.lower()
            elif counter > 0 and item.isupper() == True:
                text += "_"+item.lower()
            else:
                text += item.lower()
        if self.stateful is True:
            begin = text + "_begin"
            success = text + "_success"
            error = text + "_error"
            return [begin, success, error]
        else:
            return [text]

    def __repr__(self):
        return str(self.namespaces)

    

class Project:
    class Dirs:            
        def __init__(self):
            self.base       = os.getcwd()
            self.src        = None
            self.components = None
            self.reducers   = None
            self.set_dirs()

        def set_dirs(self):
            self.src        = os.path.abspath("src")
            os.chdir(self.src)
            self.components = os.path.abspath("components")
            self.reducers   = os.path.abspath("reducers")
            os.chdir(self.base)
            

        
    def __new__(cls):
        cd = os.getcwd().split("\\")[-1]
        return super(Project, cls).__new__(cls)

        
            
    def __init__(self):
        self.dirs = self.Dirs()
        self.components = []
        self.reducers   = []

        self._set_components()
        self._set_reducers()
        
        
    def _ls(self):
        return os.listdir(os.getcwd())
    
    def _set_components(self):
        self.components = []
        os.chdir(self.dirs.components)
        for component in self._ls():
            self.components.append((component.split(".")[0]   ,os.path.abspath(component))   )

    def _set_reducers(self):
        self.reducers = []
        os.chdir(self.dirs.reducers)
        for reducer in self._ls():
            if reducer.startswith("reducer_"):
                self.reducers.append( ( reducer.split("_")[1] ,os.path.abspath(reducer)) )

    def create_component(self, component_name="default"):
        os.chdir(self.dirs.components)
        name = component_name[0].upper() + component_name[1:]
        with open(name+"Component.tsx", "w") as f:
            f.write(templates.component(name))
        self._set_components()
        os.chdir(self.dirs.src)
        with open("Master.tsx", "r") as f: data = f.read()
        f = open("Master.tsx", "w")
        f.write(f'import {component_name}Component from "./components/{component_name}Component" \n'+data)
        f.close()
        

    def create_reducer(self, reducer_name= "default"):
        os.chdir(self.dirs.reducers)
        os.mkdir("reducer_"+ reducer_name.lower())
        os.chdir("reducer_"+reducer_name.lower())
        with open(reducer_name[0].upper()+reducer_name[1:]+"Reducer.tsx", "w") as f:
            f.write(templates.reducer(reducer_name))
            f.close()
        with open(reducer_name[0].upper()+reducer_name[1:]+"Types.tsx", "w") as f:
            f.write(templates.types(reducer_name))
            f.close()     
        with open(reducer_name[0].upper()+reducer_name[1:]+"Actions.tsx", "w") as f:
            f.write(templates.actions(reducer_name))
            f.close()

        self._set_reducers()
        self.connect_reducer(reducer_name)

        
        

 
    def connect_reducer(self, reducer_name):
        
        name = reducer_name[0].upper()+reducer_name[1:]
     
        result = ""
        with open("ConfigureStore.tsx", "r") as f:
            cur = f.read()
            necesary_index = cur.find("combineReducers({")+ "combineReducers({".__len__()+1 
            result += cur[:necesary_index]

            result += f"    {name}Reducer,\n"
            result += cur[necesary_index:]

        with open("ConfigureStore.tsx", "w") as f:
             f.write(result)

        result = "import {"+ name+"Reducer} from './reducer_"+name.lower()+"/"+name+"Reducer' ;\n"

        with open("ConfigureStore.tsx", "r") as f:
            result+= f.read()

        with open("ConfigureStore.tsx", "w") as f:
            f.write(result)

        os.chdir('actions')
        allactionstypes = ""
        with open('AllActionsTypes.tsx', 'r') as f:
            content = f.read()

        allactionstypes+="import {"+ name+"ActionTypes} from '../reducer_"+name.lower()+f"/{name}Actions';\n"

        index_start = content.find("export type AllActionTypes=")
        index_end = index_start + len("export type AllActionTypes=")

        allactionstypes +=content[:index_end]
        allactionstypes += f"\n        | {name}ActionTypes"

        allactionstypes+=content[index_end:]
                
            
        with open('AllActionsTypes.tsx', 'w') as f:
            f.write(allactionstypes)

        with open('AllActions.tsx', 'r') as f:
            content = f.read()

        result = f"import * as {name.lower()}Constants from '../reducer_{name.lower()}/{name}Actions'\n"
        result += content

        with open('AllActions.tsx', 'w') as f:
            f.write(result)        
        
        
        
    def create_action(self, action="MakeTest", reducer="default", stateful=False):
        os.chdir(self.dirs.reducers+r"\\reducer_"+reducer.lower())
        
        a_file = reducer[0].upper()+reducer[1:]+"Actions.tsx"
        r_file = reducer[0].upper()+reducer[1:]+"Reducer.tsx"
        t_file = reducer[0].upper()+reducer[1:]+"Types.tsx"
        extension = ""
        template = Template(action, stateful=stateful)
        with open(a_file, "r") as f:
            content = f.readlines()

        interfaces = content.index("//INTERFACES\n")

        types = content.index("//TYPES\n")

        for element in template._snake_case():
            extension += f"export const {element.upper()} = '{element.upper()}';\n"

            
        for i in content[:interfaces]:
            extension+=i
         
        extension+="//INTERFACES\n"    
        #queryOne = r"//INTERFACES"
        #indexOne = int(content.find(queryOne))+len(queryOne)
        #extension += content[: indexOne] + "\n"
        for counter, element in enumerate(template._camel_case()):
            extension += f'export interface {element}{"{"}\n    type: typeof {template.namespaces["snake_case"][counter].upper()}\n{"}"}\n '
        for i in content[interfaces+1: types]:
            extension+=i

        
        
        for i in content[types: types+2]:
            extension+=i
        
        #queryTwo = f"export type {reducer}ActionTypes="
        #indexTwo = int(content.find(queryTwo)) + len(queryTwo)    
        #extension += content[indexOne:indexTwo]
  
        for element in template._camel_case():
            extension += f"    | {element} \n"
        extension += "".join(content[types+2:])

        with open(a_file, "w") as f:
            f.write(extension)

 
        with open(r_file, "r") as f:
            content = f.read()

        reducer_temp = ""
        breakpoint = "switch(action.type){\n"
        checkpoint = content.find(breakpoint)
        reducer_temp += content[:checkpoint+len(breakpoint)]+"\n"

        for element in template._snake_case():
            reducer_temp += f'''        case constants.{element.upper()}:\n            return state;\n'''
        reducer_temp += content[checkpoint+len(breakpoint):]

        with open(r_file, "w") as f:
            f.write(reducer_temp)

        os.chdir(self.dirs.reducers)
        os.chdir('actions')
        with open('AllActions.tsx') as f:
            content = f.readlines()

        methods = content.index("//METHODS\n")
        data = ""
        for line in content[:methods+1]:
            data+=line

        for counter, element in enumerate(template._camel_case()):
            data+=f'''export const {element}=():AllAppActions=>({"{"}
                type: {reducer.lower()}Constants.{template.namespaces["snake_case"][counter].upper()}\n{"}"})
            '''
        for line in content[methods+1:]:
            data+=line

        with open("AllActions.tsx", "w") as f:
            f.write(data)
            
        
        
        
        
        

def main():
    proj = Project()
    
 
    for counter, arg in enumerate(sys.argv):
        if arg=="create-component":
            try:
                component_name = sys.argv[counter+1]
                component_name = component_name[0].upper() + component_name[1:]
                proj.create_component(component_name)
                
            except:
                print("Please enter component name", file = sys.stderr)
        if arg=="create-reducer":
            reducer_name = sys.argv[counter+1]
            proj.create_reducer(reducer_name)
    
                                                                                                                                                 
        if arg=="create-action":
            action_name = sys.argv[counter+1]
            reducer_name = sys.argv[counter+2].lower()                
            if "-stateful" in sys.argv:
                proj.create_action(action_name, reducer_name, stateful=True)
            else:
                proj.create_action(action_name, reducer_name, stateful=False)

        if arg=="debug":
            print(os.getcwd()) 


        

if __name__=="__main__":
    main()

                
            
            
        

    

    


 
