import { s3 } from "./core/S3Client";

import { putCommand, getCommand, deleteCommand } from "./core/command"
import { downloadBlobAction, keyGenerator } from "./core/utils"

export const storageUploadFile = (file: File, bucketName: string, key: string): Promise<void> => {
  return putCommand(s3, {
    Bucket: bucketName,
    Key: key,
    Body: file,
    ContentType: file.type,
  });
};

export const storageDownloadFile = (bucketName: string, key: string): Promise<Blob | undefined> => {
  return getCommand(s3, {
    Bucket: bucketName,
    Key: key,
  });
};

export const storageDeleteFile = (bucketName: string, key: string): Promise<void> => {
  return deleteCommand(s3, {
    Bucket: bucketName,
    Key: key,
  });
}

export const storageOpenDownloadedBlob = (blob: Blob, downloadName: string) => {
  downloadBlobAction(blob, downloadName);
}

export const storageGenerateKey = (filename: string): string => {
  return keyGenerator(filename);
}
