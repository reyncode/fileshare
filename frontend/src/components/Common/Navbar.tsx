import {
  Button, 
  Flex, 
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from "@chakra-ui/react"
import { FaFileAlt } from "react-icons/fa"
import { ChevronDownIcon } from '@chakra-ui/icons'
import { useFilePicker } from 'use-file-picker';
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  type ApiError, 
  type FileCreate, 
  FilesMetadataService, 
  FilesStorageService 
} from "../../client"

const Navbar = () => {
  const bucketName = import.meta.env.VITE_FILE_BUCKET_URL;
  const queryClient = useQueryClient()
  const mutation = useMutation({
    mutationFn: (files: File[]) => {
      const handleFileUpload = async (file: File) => {
        const key = FilesStorageService.generateKey(file.name)
        
        await FilesStorageService.uploadFile(file, bucketName, key);

        const metadata: FileCreate = {
          name: file.name,
          access_key: key,
          size: file.size
        };

        return FilesMetadataService.createFile({ requestBody: metadata });
      };

      // process each file in parallel
      return Promise.all(files.map(file => handleFileUpload(file)));
    },
    onSuccess: () => {
      console.log("success")
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail || "An unknown error occurred";
      console.log(errDetail)
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
