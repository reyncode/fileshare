import { PutObjectCommandOutput, GetObjectCommandOutput, DeleteObjectCommandOutput } from "@aws-sdk/client-s3";

export class S3Error extends Error {
  public readonly operation: string;
  public readonly status: number;
  public readonly statusText: string;
  public readonly requestId: string;
  public readonly body: unknown;

  constructor(operation: string, response: PutObjectCommandOutput | GetObjectCommandOutput | DeleteObjectCommandOutput, message: string) {
    super(message);

    this.name = 'S3Error';
    this.operation = operation;
    this.status = response.$metadata.httpStatusCode!;
    this.statusText = message;
    this.requestId = response.$metadata.requestId!;
    this.body = response;
  }
}
