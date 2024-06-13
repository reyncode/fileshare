export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
}

export const namePattern = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Invalid name",
}

export const passwordRules = (isRequired = true) => {
  const rules: any = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  }

  if (isRequired) {
    rules.required = "Password is required"
  }

  return rules
}

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true,
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password
      return value === password ? true : "The passwords do not match"
    },
  }

  if (isRequired) {
    rules.required = "Password confirmation is required"
  }

  return rules
}

export const datetimeFormatter = (str: string | null | undefined) => {
  if ((str === null) || (str === undefined)) {
    return "";
  }

  const date = new Date(str);
  return date.toLocaleString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit"
  });
}

export const formatBytes = (bytes: number) => {
  var marker = 1024;
  var decimal = 2;
  var kiloBytes = marker;
  var megaBytes = marker * marker;
  var gigaBytes = marker * marker * marker;

  if(bytes < kiloBytes) return bytes + " Bytes";
  else if(bytes < megaBytes) return(bytes / kiloBytes).toFixed(decimal) + " KB";
  else if(bytes < gigaBytes) return(bytes / megaBytes).toFixed(decimal) + " MB";
  else return(bytes / gigaBytes).toFixed(decimal) + " GB";
}
