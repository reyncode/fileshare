import { v4 as uuidv4 } from 'uuid';

export const isBlob = (value: any): value is Blob => {
	return value instanceof Blob;
};

export const downloadBlobAction = (blob: Blob, downloadName: string): void => {
  if (isBlob(blob)) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');

    a.href = url;
    a.download = downloadName;

    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } else {
    console.error("Arg provided to download action was not an instance of Blob");
  }
};

export const keyGenerator = (filename: string): string => {
  const uniqueId = uuidv4();
  const extension = filename.split('.').pop();
  const date = new Date().toISOString().split('T')[0];

  return `${date}/${uniqueId}.${extension}`
}
