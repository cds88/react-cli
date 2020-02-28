import os

BASE_DIR = os.getcwd()
babelrc = '''
{
    "presets": [
        "@babel/preset-env",
        "@babel/preset-react"
    ],
    "plugins": [
        "transform-class-properties",
        "transform-object-rest-spread"
    ]
}
'''
index = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    

    <div id="app"></div>

    
<!-- "build": "webpack-dev-server --entry ./public/Index.js --output-filename ./dist/bundle.js", -->
</body>
</html>
'''
packagejson='''
{
    "name": "projekt_v3",
    "version": "1.0.0",
    "main": "index.js",
    "scripts": {
    "webpack": "webpack",
    
    "build:prod": "webpack public/Index.js dist/bundle.js -p",
    "start": "webpack-dev-server --mode development --open --hot",
    "build": "webpack --mode production"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "devDependencies": {
    "@babel/core": "^7.6.4",
    "@babel/preset-env": "^7.6.3",
    "@babel/preset-es2017": "^7.0.0-beta.53",
    "@babel/preset-react": "^7.6.3",
    "@emotion/core": "^10.0.22",
    "@types/react": "^16.9.9",
    "@types/react-dom": "^16.9.2",
    "@types/react-redux": "^7.1.5",
    "@types/styled-components": "^4.1.19",
    "babel-loader": "^8.0.6",
    "babel-plugin-transform-class-properties": "^6.24.1",
    "babel-plugin-transform-object-rest-spread": "^6.26.0",
    "bootstrap": "^4.3.1",
    "css-loader": "^3.2.0",
    "emotion": "^10.0.23",
    "html-webpack-plugin": "^3.2.0",
    "node-sass": "^4.12.0",
    "source-map-loader": "^0.2.4",
    "ts-loader": "^6.2.0",
    "typescript": "^3.6.4",
    "webpack": "^4.41.2",
    "webpack-cli": "^3.3.9",
    "webpack-dev-server": "^3.10.3"
    },
    "dependencies": {
    "@types/react-router-dom": "^5.1.2",
    "@types/react-slick": "^0.23.4",
    "@types/react-transition-group": "^4.2.3",
    "@types/styled-components": "^4.1.19",
    "@zeit/next-css": "^1.0.1",
    "axios": "^0.19.0",
    "css-loader": "^3.2.0",
    "file-loader": "^4.2.0",
    "jquery": "^3.4.1",
    "prop-types": "^15.7.2",
    "react": "^16.10.2",
    "react-dom": "^16.10.2",
    "react-redux": "^7.1.1",
    "react-router-dom": "^5.1.2",
    "react-slick": "^0.25.2",
    "react-transition-group": "^4.3.0",
    "redux": "^4.0.4",
    "redux-thunk": "^2.3.0",
    "sass-loader": "^8.0.0",
    "slick-carousel": "^1.8.1",
    "style-loader": "^1.0.0",
    "styled-components": "^4.4.0",
    "thunk": "0.0.1",
    "url-loader": "^2.2.0"
    },
    "description": ""
}
'''
tsconfig = '''
{
    "compilerOptions": {
        "outDir": "./dist/",
        "sourceMap": true,
        "noImplicitAny": true,
        "module": "commonjs",
        "target": "es2017",
        "jsx": "react",
        "lib": [
            "es2017",
            "dom"
        ]
    }
}
'''
webpackconfig = '''

const path = require('path');
const HtmlWebpackPlugin = require("html-webpack-plugin");



module.exports = {
    entry: {
        Index: './src/Index.tsx'
    },
    watch: true,
    devtool: false,
    //'source-map',
    output: { 
        filename: '[name].js',
        path: path.resolve(__dirname, './public/')
    },
    cache: true,
    mode: 'development',
    plugins:[
        new HtmlWebpackPlugin({
            template: './index.html'
        })
    ],


    module: {
        rules: [

            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.ts(x?)$/,
                exclude: /node_modules/,
                use: {
                    loader: "ts-loader"
                }
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.s[ac]ss$/i,
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
            {
                test: /\.(png|jpe?g|gif|eot|ttf|woff|svg)$/i,
                use: [
                    {
                        loader: 'file-loader',
                    },
                ],
            }


        ]



    },
    resolve: {
        extensions: [
            '.tsx', '.ts', '.js'
        ]
    },
    devServer:{
        contentBase: path.join(__dirname, 'src'),
        compress: true,
        port : 4800
    }

}
'''

src_app='''
import * as React from 'react';

import { Provider } from 'react-redux'; 
    
import Master from './Master';

import { store } from "./reducers/ConfigureStore";

const App: React.FC = () => {
    return (
            <Provider store={store}>
            <Master />
            </Provider>
    )
}

export default App;
'''
src_index='''
import * as React from 'react';
import * as ReactDOM from 'react-dom';

import App from './App';




ReactDOM.render(
    <App />, document.getElementById("app")
);



'''
src_master='''
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { AppState } from "./reducers/ConfigureStore";
import styled from "styled-components";
import { bindActionCreators } from 'redux';
import { AllAppActions } from './reducers/actions/AllActionsTypes';
import { connect } from 'react-redux';
import { ThunkDispatch } from "redux-thunk";

export interface MasterProps {

}
interface LinkStateToProps{
}
const mapStateToProps =(state:AppState, ownProps: MasterProps):LinkStateToProps=>
({})

interface LinkDispatchToProps{
}

const mapDispatchToProps =( dispatch: ThunkDispatch<any, any, AllAppActions>,
ownProps: MasterProps): LinkDispatchToProps=>({})

type Props = MasterProps & LinkStateToProps & LinkDispatchToProps;
const Master=(Props:Props)=> {



        return (
                <h1>  Hello </h1>
        );

}

export default connect(null, null)( Master);



'''
#REDUX
configure_store ='''
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk, { ThunkMiddleware } from "redux-thunk";
    

import { AllAppActions } from "./actions/AllActionsTypes";

export const rootReducer = combineReducers({
        
});

export type AppState = ReturnType<typeof rootReducer>;

export const store = createStore(
    rootReducer,
    applyMiddleware(thunk as ThunkMiddleware<AppState, AllAppActions>)
);


'''
all_actions_types='''

export type AllActionTypes=
        | null


export type AllAppActions = AllActionTypes
'''
all_actions='''
import {AllAppActions} from './AllActionsTypes';\n


//METHODS\n



'''
with open('.babelrc', 'w') as f:
    f.write(babelrc)
with open('index.html', 'w') as f:
    f.write(index)
with open('package.json', 'w') as f:
    f.write(packagejson)
with open('tsconfig.json', 'w') as f:
    f.write(tsconfig)
with open('webpack.config.js', 'w') as f:
    f.write(webpackconfig)

os.mkdir("src")
os.mkdir("public")
os.chdir("src")
os.mkdir("components")
os.mkdir("reducers")
os.mkdir("styles")

with open("App.tsx", "w") as f:
    f.write(src_app)
with open("Index.tsx", "w") as f:
    f.write(src_index)
with open("Master.tsx", "w") as f:
    f.write(src_master)
    

os.chdir('reducers')
with open("ConfigureStore.tsx", "w") as f:
    f.write(configure_store)

os.mkdir("actions")
os.chdir("actions")
with open("AllActions.tsx", "w") as f:
    f.write(all_actions)
with open("AllActionsTypes.tsx", "w") as f:
    f.write(all_actions_types)
    

os.chdir(BASE_DIR)
os.system('npm init -y && npm install')



