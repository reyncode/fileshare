import AWS from "aws-sdk";
import config from "../config"

const s3 = new AWS.S3({
    accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
    region: process.env.REACT_APP_AWS_REGION,
    endpoint: config.REACT_APP_STORAGE_URL,
    s3ForcePathStyle: true,
});

export default s3;
