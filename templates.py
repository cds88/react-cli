def braces(name):
    return f'{"{"}'+name+f'{"}"}'

def component(component_name="defaultTitle"):
    component_name = component_name[0].upper() + component_name[1:]
    COMPONENT_TEMPLATE=f'''
    import * as React from "react";
 

    import {"{"} AllAppActions {"}"} from '../reducers/actions/AllActionsTypes';

    import {"{"} ThunkDispatch {"}"}  from "redux-thunk";
    import {"{"} bindActionCreators {"}"}  from 'redux';
    import {"{AppState}"} from "../reducers/ConfigureStore";
    import {"{connect}"} from 'react-redux';

    export interface {component_name}Props{"{}"}

    interface LinkStateToProps{"{}"}

    const mapStateToProps=(state:AppState,
    ownProps:{component_name}Props):LinkStateToProps=>
    ({"{"} {"}"} ) 

    interface LinkDispatchToProps{"{}"}

    const mapDispatchToProps=(
        dispatch: ThunkDispatch<any, any, AllAppActions>,
        ownProps: {component_name}Props
    ):LinkDispatchToProps=>({"{}"})

    type Props ={component_name}Props & LinkStateToProps & LinkDispatchToProps;

    const {component_name}Component=(Props:Props)=>{"{"}
    return(
        <div> </div>
    )
    
    {"}"}

    export default connect(null, null)({component_name}Component)
    '''
    
    return COMPONENT_TEMPLATE

def reducer(reducer_name):
    name = reducer_name[0].upper()+reducer_name[1:]
    REDUCER_TEMPLATE = f'''
import {braces("I"+name+"State")} from "./{name}Types";
import {braces(name+"ActionTypes" )} from "./{name}Actions";
import * as constants from './{name}Actions';

const {name}ReducerDefaultState : I{name}State = {"{"}
{"}"}


const {name}Reducer=(
        state = {name}ReducerDefaultState,
        action: {name}ActionTypes
        ):I{name}State => {"{"}
            switch(action.type){"{"}
                default:
                    return state;
            {"}"}
        {"}"}

        
export {braces(name+"Reducer")}


'''
    return REDUCER_TEMPLATE

def actions(reducer_name):
    name = reducer_name[0].upper()+reducer_name[1:]
    ACTIONS_TEMPLATE = f'''




//INTERFACES





//TYPES
export type {name}ActionTypes=
    | null

export type AppActions = {name}ActionTypes;


'''

    return ACTIONS_TEMPLATE

def types(reducer_name):
    name = reducer_name[0].upper()+reducer_name[1:]
    TYPES_TEMPLATE=f'''

export interface I{name}State{"{"}

{"}"}

'''
    return TYPES_TEMPLATE

class template:

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




