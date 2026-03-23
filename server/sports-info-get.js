import axios from 'axios'
import * as cheerios from 'cheerio'
import {
    SecretsManagerClient,
    GetSecretValueCommand,
    } from "@aws-sdk/client-secrets-manager";


const URL = get_URL()
async function get_URL(){
    const secret_name = "Sports-URL";

    const client = new SecretsManagerClient({
    region: "us-east-2",
    });

    let response;

    try {
    response = await client.send(
        new GetSecretValueCommand({
        SecretId: secret_name,
        VersionStage: "AWSCURRENT", // VersionStage defaults to AWSCURRENT if unspecified
        })
    );
    } catch (error) {
    // For a list of exceptions thrown, see
    // https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    throw error;
    }

    const secret = response.SecretString;
    return secret
}
export const handler = async (_event, context) => {

    if (context.getRemainingTimeInMillis < 100){
        console.log("Less than 100ms Remaining : Timing out")
        return time_out_message = {
            statusCode: 500,
            body: "Fuction timed out before completion"
        }
    }
    try{
        result = await axios.get(URL, {
            timeout: 5000, // 5 second timeout so Lambda doesn't hang
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0' }
        })

        
    }
    catch (error){
        console.log("Error in fetching : " + URL)
        console.log(`Error message : ${error}`)
        return {
            "statusCode" : 500,
            "error" : error
        }
    }
    
    
    

}