import { 
  S3Client,
  PutObjectCommand,
  PutObjectCommandInput,
  GetObjectCommand,
  GetObjectCommandInput,
  DeleteObjectCommand,
  DeleteObjectCommandInput,
} from "@aws-sdk/client-s3";

export const putCommand = async (client: S3Client, input: PutObjectCommandInput): Promise<void> => {
  try {
    const command = new PutObjectCommand(input);
    await client.send(command);
  } catch (error) {
    throw new Error(`${(error as Error).message}`)
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
    throw new Error(`${(error as Error).message}`)
  }
}

export const deleteCommand = async (client: S3Client, input: DeleteObjectCommandInput): Promise<void> => {
  try {
    const command = new DeleteObjectCommand(input);
    await client.send(command);
  } catch (error) {
    throw new Error(`${(error as Error).message}`)
  }
}
