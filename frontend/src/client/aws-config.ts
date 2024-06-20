import AWS from "aws-sdk";
import config from "../config"

const s3 = new AWS.S3({
    accessKeyId: "access-key-id",
    secretAccessKey: "secret-access-key",
    region: "ca-central-1",
    endpoint: config.REACT_APP_STORAGE_URL,
    s3ForcePathStyle: true,
});

export default s3;
