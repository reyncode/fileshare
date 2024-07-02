import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';
import { 
  PutObjectCommand, 
  GetObjectCommand, 
  DeleteObjectCommand 
} from '@aws-sdk/client-s3';
import s3 from "./aws-config"
import { v4 as uuidv4 } from 'uuid';

import type { 
  Body_login_login_access_token,
  Message,
  NewPassword,
  Token,
  UserPublic,
  UpdatePassword,
  UserCreate,
  UserUpdate,
  FileCreate,
  FilePublic,
  FilesPublic,
  FileUpdate 
} from './models';

export type TDataLoginAccessToken = { 
  formData: Body_login_login_access_token;
}

export type TDataResetPassword = { 
  requestBody: NewPassword;
}

export class LoginService {

	/**
	 * Login Access Token
	 * OAuth2 compatible token login, get an access token for future requests
	 * @returns Token Successful Response
	 * @throws ApiError
	 */
	public static loginAccessToken(data: TDataLoginAccessToken): CancelablePromise<Token> {
		const { formData } = data;

		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/login/access-token',
			formData: formData,
			mediaType: 'application/x-www-form-urlencoded',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Test Token
	 * Test access token
	 * @returns UserPublic Successful Response
	 * @throws ApiError
	 */
	public static testToken(): CancelablePromise<UserPublic> {
      return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/login/test-token',
		});
	}

	/**
	 * Reset Password
	 * Reset password
	 * @returns Message Successful Response
	 * @throws ApiError
	 */
	public static resetPassword(data: TDataResetPassword): CancelablePromise<Message> {
		const { requestBody } = data;

		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/reset-password/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}
}

export type TDataReadUsers = {
  limit?: number;
  skip?: number;
}

export type TDataCreateUser = {
  requestBody: UserCreate;
}

export type TDataUpdateUser = {
  requestBody: UserUpdate;
}

export type TDataUpdatePasswordMe = {
  requestBody: UpdatePassword;
}

export type TDataReadUserById = {
  userId: number;
}

export class UsersService {

	/**
	 * Create User
	 * Create new user.
	 * @returns UserPublic Successful Response
	 * @throws ApiError
	 */
	public static createUser(data: TDataCreateUser): CancelablePromise<UserPublic> {
		const { requestBody } = data;

		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/users/register',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read User Me
	 * Get current user.
	 * @returns UserPublic Successful Response
	 * @throws ApiError
	 */
	public static readUserMe(): CancelablePromise<UserPublic> {
				return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/users/me',
		});
	}

	/**
	 * Update User Me
	 * Update own user.
	 * @returns UserPublic Successful Response
	 * @throws ApiError
	 */
	public static updateUser(data: TDataUpdateUser): CancelablePromise<UserPublic> {
		const { requestBody } = data;

		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/api/v1/users/me',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Update Password Me
	 * Update own password.
	 * @returns Message Successful Response
	 * @throws ApiError
	 */
	public static updatePasswordMe(data: TDataUpdatePasswordMe): CancelablePromise<Message> {
		const { requestBody } = data;

		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/api/v1/users/me/password',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read User By Id
	 * Get a specific user by id.
	 * @returns UserPublic Successful Response
	 * @throws ApiError
	 */
	public static readUserById(data: TDataReadUserById): CancelablePromise<UserPublic> {
		const { userId } = data;

		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/users/{user_id}',
			path: {
				user_id: userId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Delete User
	 * Delete own account.
	 * @returns Message Successful Response
	 * @throws ApiError
	 */
	public static deleteUser(): CancelablePromise<Message> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/users/me',
			errors: {
				422: `Validation Error`,
			},
		});
	}

}

export type TDataReadFiles = {
                limit?: number
skip?: number
                
            }
export type TDataCreateFile = {
                requestBody: FileCreate
                
            }
export type TDataReadFile = {
                id: number
                
            }
export type TDataUpdateFile = {
                id: number
requestBody: FileUpdate
                
            }
export type TDataDeleteFile = {
                id: number
                
            }

export class FilesMetadataService {

	/**
	 * Read Files
	 * Retrieve files.
	 * @returns FilesPublic Successful Response
	 * @throws ApiError
	 */
	public static readFiles(data: TDataReadFiles = {}): CancelablePromise<FilesPublic> {
		const {
limit = 25,
skip = 0,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/files/',
			query: {
				skip, limit
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Create File
	 * Create new file.
	 * @returns FilePublic Successful Response
	 * @throws ApiError
	 */
	public static createFile(data: TDataCreateFile): CancelablePromise<FilePublic> {
		const { requestBody } = data;

		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/files/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read File
	 * Get file by ID.
	 * @returns FilePublic Successful Response
	 * @throws ApiError
	 */
	public static readFile(data: TDataReadFile): CancelablePromise<FilePublic> {
		const {
id,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/files/{id}',
			path: {
				id
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Update File
	 * Update a file.
	 * @returns FilePublic Successful Response
	 * @throws ApiError
	 */
	public static updateFile(data: TDataUpdateFile): CancelablePromise<FilePublic> {
		const {
id,
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/api/v1/files/{id}',
			path: {
				id
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

  /**
   * Delete File
   * Delete a file.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteFile(data: TDataDeleteFile): CancelablePromise<Message> {
    const { id, } = data;

    return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/files/{id}',
			path: {
				id
			},
			errors: {
				422: `Validation Error`,
			},
    });
	}
}

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
