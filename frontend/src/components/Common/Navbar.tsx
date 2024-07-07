import { useRef } from 'react';
import {
  Button, 
  Flex, 
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useToast,
  ToastId,
} from "@chakra-ui/react"
import { FaFileAlt } from "react-icons/fa"
import { ChevronDownIcon } from '@chakra-ui/icons'
import { useFilePicker } from 'use-file-picker';
import { useMutation, useQueryClient } from "@tanstack/react-query";
import config from "../../config"
import { type ApiError, type FileCreate, filesCreateFile } from '../../client/axios';
import { storageUploadFile, storageGenerateKey } from '../../client/s3';

const Navbar = () => {
  const bucketName = config.REACT_APP_FILE_BUCKET_NAME;
  const queryClient = useQueryClient()
  const toast = useToast()
  const toastIdRef = useRef<ToastId | undefined>(undefined);
  const mutation = useMutation({
    mutationFn: (files: File[]) => {
      toastIdRef.current = toast({
        title: `Uploading`,
        description: `Files are being uploaded`,
        status: "info",
        isClosable: true,
        position: "bottom-right",
        duration: null,
      })

      const handleFileUpload = async (file: File) => {
        const key = storageGenerateKey(file.name);
        
        await storageUploadFile(file, bucketName, key);

        const metadata: FileCreate = {
          name: file.name,
          access_key: key,
          size: file.size
        };

        return filesCreateFile({ requestBody: metadata })
      };

      // process each file in parallel
      return Promise.all(files.map(file => handleFileUpload(file)));
    },
    onSuccess: () => {
      if (toastIdRef.current) {
        toast.update(toastIdRef.current, {
          title: "Success",
          description: "All files uploaded successfully",
          status: "success",
          isClosable: true,
          position: "bottom-right",
          duration: 5000,
        })
      } else {
        console.error('Toast ID is undefined');
      }
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail || (err.message as any);
      if (toastIdRef.current) {
        toast.update(toastIdRef.current, {
          title: "Error",
          description: `${errDetail}`,
          status: "error",
          isClosable: true,
          position: "bottom-right",
          duration: 5000,
        })
      } else {
        console.error('Toast ID is undefined');
      }
      console.error(errDetail)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["files"] })
    },
  })

  const { openFilePicker } = useFilePicker({
    accept: "*",
    onFilesSelected: ({ plainFiles }) => {
      mutation.mutate(plainFiles)
    },
  });

  return (
    <>
      <Flex py={8} gap={4}>
        <Menu>
          <MenuButton 
            as={Button} 
            rightIcon={<ChevronDownIcon />}
          >
            New
          </MenuButton>
          <MenuList>
            <MenuItem 
              icon={<FaFileAlt />}
              onClick={() => {openFilePicker()}}
            >
              File Upload
            </MenuItem>
          </MenuList>
        </Menu>
      </Flex>
    </>
  )
}

export default Navbar
