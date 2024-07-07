import { 
  S3Client,
  PutObjectCommand,
  PutObjectCommandInput,
  PutObjectCommandOutput,
  GetObjectCommand,
  GetObjectCommandInput,
  GetObjectCommandOutput,
  DeleteObjectCommand,
  DeleteObjectCommandInput,
  DeleteObjectCommandOutput
} from "@aws-sdk/client-s3";

import { S3Error } from "./S3Error"

export const isCommandOutput = (error: any): error is PutObjectCommandOutput | GetObjectCommandOutput | DeleteObjectCommandOutput => {
  return error && typeof error === "object" && "$metadata" in error;
}

export const putCommand = async (client: S3Client, input: PutObjectCommandInput): Promise<void> => {
  try {
    const command = new PutObjectCommand(input);
    await client.send(command);
  } catch (error) {
    if (isCommandOutput(error)) {
      throw new S3Error("PutObject", error, "File upload failed");
    }
  }
}

export const getCommand = async (client: S3Client, input: GetObjectCommandInput): Promise<Blob | undefined> => {
  try {
    const command = new GetObjectCommand(input);
    const response = await client.send(command);

    const streamToBlob = async (stream: any): Promise<Blob> => {
      const chunks = [];
      for await (const chunk of stream) {
        chunks.push(chunk);
      }
      const blob = new Blob(chunks);
      return blob;
    };

    return await streamToBlob(response.Body);
  } catch (error) {
    if (isCommandOutput(error)) {
      throw new S3Error("GetObject", error, "File download failed");
    }

    return undefined;
  }
}

export const deleteCommand = async (client: S3Client, input: DeleteObjectCommandInput): Promise<void> => {
  try {
    const command = new DeleteObjectCommand(input);
    await client.send(command);
  } catch (error) {
    if (isCommandOutput(error)) {
      throw new S3Error("DeleteObject", error, "File delete failed");
    }
  }
}
