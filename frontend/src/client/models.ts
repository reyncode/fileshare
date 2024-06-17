export type Body_login_login_access_token = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};


export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};


export type FileCreate = {
	name: string;
  access_key: string;
  size?: number | null;
};


export type FilePublic = {
	name: string;
  access_key: string;
  size: number;
  created_at?: string | null;
  updated_at?: string | null;
	id: number;
	owner_id: number;
};


export type FileUpdate = {
	name?: string | null;
  accessKey?: string | null;
  size?: number | null;
};


export type FilesPublic = {
	data: Array<FilePublic>;
	count: number;
};


export type Message = {
	message: string;
};


export type NewPassword = {
	token: string;
	new_password: string;
};


export type Token = {
	access_token: string;
	token_type?: string;
};


export type UpdatePassword = {
	current_password: string;
	new_password: string;
};


export type UserCreate = {
	email: string;
	password: string;
};


export type UserPublic = {
	email: string;
  created_at?: string | null;
  updated_at?: string | null;
	id: number;
};


export type UserUpdate = {
	email?: string | null;
};


export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};

