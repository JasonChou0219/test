import { writeFile } from 'fs';

// Configure Angular `environment.ts` file path
const targetPath = './src/environments/environment.ts';

// Load node modules
const colors = require('colors');
require('dotenv').load();

// `environment.ts` file structure
const env = process.env.ANGULAR_APP_ENV;
//let envConfigFile = '// test';
let envConfigFile = env;
if (env === 'production') {
    const envConfigFile = `export const env = '${process.env.ANGULAR_APP_ENV}';
        envApiUrl = \`https://${process.env.ANGULAR_APP_DOMAIN_PROD}\`;
        export const apiUrl = envApiUrl;
        export const appName = '${process.env.ANGULAR_APP_NAME}';
    // apiBaseUrl: '${process.env.API_BASE_URL}',
    // apiUrl: '${process.env.API_URL}',
    // appName: '${process.env.APP_NAME}',
    // awsPubKey: '${process.env.AWSKEY}',
    // nodeEnv: '${process.env.NODE_ENV}',
    // production: '${process.env.PRODUCTION}'
    `;
} else if (env === 'staging') {
    const envConfigFile = `export const env = '${process.env.ANGULAR_APP_ENV}';
        envApiUrl = \`https://${process.env.ANGULAR_APP_DOMAIN_STAG}\`;
        export const apiUrl = envApiUrl;
        export const appName = '${process.env.ANGULAR_APP_NAME}';
    // apiBaseUrl: '${process.env.API_BASE_URL}',
    // apiUrl: '${process.env.API_URL}',
    // appName: '${process.env.APP_NAME}',
    // awsPubKey: '${process.env.AWSKEY}',
    // nodeEnv: '${process.env.NODE_ENV}',
    // production: '${process.env.PRODUCTION}'
    `;
} else {
    const envConfigFile = `export const env = '${process.env.ANGULAR_APP_ENV}';
        envApiUrl = \`https://${process.env.ANGULAR_APP_DOMAIN_DEV}\`;
        export const apiUrl = envApiUrl;
        export const appName = '${process.env.ANGULAR_APP_NAME}';
    // apiBaseUrl: '${process.env.API_BASE_URL}',
    // apiUrl: '${process.env.API_URL}',
    // appName: '${process.env.APP_NAME}',
    // awsPubKey: '${process.env.AWSKEY}',
    // nodeEnv: '${process.env.NODE_ENV}',
    // production: '${process.env.PRODUCTION}'
    `;
}

/*
const envConfigFile = `export const env = '${process.env.ANGULAR_APP_ENV}';
let envApiUrl = '';
if (env === 'production') {
    envApiUrl = \`https://${process.env.ANGULAR_APP_DOMAIN_PROD}\`;
} else if (env === 'staging') {
    envApiUrl = \`https://${process.env.ANGULAR_APP_DOMAIN_STAG}\`;
} else {
    envApiUrl = \`http://${process.env.ANGULAR_APP_DOMAIN_DEV}\`;
}

export const apiUrl = envApiUrl;
export const appName = '${process.env.ANGULAR_APP_NAME}';
// apiBaseUrl: '${process.env.API_BASE_URL}',
// apiUrl: '${process.env.API_URL}',
// appName: '${process.env.APP_NAME}',
// awsPubKey: '${process.env.AWSKEY}',
// nodeEnv: '${process.env.NODE_ENV}',
// production: '${process.env.PRODUCTION}'
`;
*/

console.log(colors.magenta('The file `environment.ts` will be written with the following content: \n'));

console.log(colors.grey(envConfigFile));

writeFile(targetPath, envConfigFile, function (err) {
    if (err) {
        throw console.error(err);
    } else {
        console.log(colors.magenta(`Angular environment.ts file generated correctly at ${targetPath} \n`));
    }
});
