import { 
  PutObjectCommand, 
  GetObjectCommand, 
  DeleteObjectCommand 
} from '@aws-sdk/client-s3';
import s3 from "./aws-config"
import { v4 as uuidv4 } from 'uuid';

export class FilesStorageService {
  /**
   * Upload File
   * Upload a file.
   * @returns File Upload URL
   * @throws Error
   */
  public static async uploadFile(file: File, bucketName: string, key: string): Promise<void> {
    const params = {
      Bucket: bucketName,
      Key: key,
      Body: file,
      ContentType: file.type,
    };

    try {
      const command = new PutObjectCommand(params);
      await s3.send(command);
    } catch (error) {
      throw new Error(`File upload failed: ${(error as Error).message}`);
    }
  }

  private static openFileURL(blob: Blob, filename: string) { 
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Download File
   * Download a file.
   * @returns Void
   * @throws Error
   */
  public static async downloadFile(bucketName: string, key: string, filename: string): Promise<void> {
    const params = {
      Bucket: bucketName,
      Key: key,
    };

    try {
      const command = new GetObjectCommand(params);
      const response = await s3.send(command);

      const streamToBlob = async (stream: any) => {
        const chunks = [];
        for await (const chunk of stream) {
          chunks.push(chunk);
        }
        const blob = new Blob(chunks);
        return blob;
      };

      const blob = await streamToBlob(response.Body);

      this.openFileURL(blob, filename);

    } catch (error) {
      throw new Error(`File download failed: ${(error as Error).message}`);
    }
  }

  public static async deleteFile(bucketName: string, key: string): Promise<void> {
    const params = {
      Bucket: bucketName,
      Key: key,
    };

    try {
      const command = new DeleteObjectCommand(params);
      await s3.send(command);
    } catch (error) {
      throw new Error(`File delete failed: ${(error as Error).message}`);
    }
  }

  public static generateKey(filename: string): string {
    const uniqueId = uuidv4();
    const extension = filename.split('.').pop();
    const date = new Date().toISOString().split('T')[0];

    return `${date}/${uniqueId}.${extension}`
  }
}
