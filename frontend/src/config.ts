interface Config {
  REACT_APP_BACKEND_URL: string;
  REACT_APP_STORAGE_URL: string;
  REACT_APP_FILE_BUCKET_NAME: string;
}

const getConfig = (): Config => {
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  if (!backendURL) {
    throw new Error("Missing REACT_APP_BACKEND_URL environment variable");
  }

  const storageURL = process.env.REACT_APP_STORAGE_URL;
  if (!storageURL) {
    throw new Error("Missing REACT_APP_STORAGE_URL environment variable");
  }

  const bucketName = process.env.REACT_APP_FILE_BUCKET_NAME;
  if (!bucketName) {
    throw new Error("Missing REACT_APP_FILE_BUCKET_NAME environment variable");
  }

  return {
    REACT_APP_BACKEND_URL: backendURL,
    REACT_APP_STORAGE_URL: storageURL,
    REACT_APP_FILE_BUCKET_NAME: bucketName,
  };
};

const config = getConfig();

export default config;
