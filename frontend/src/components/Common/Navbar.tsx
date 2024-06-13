import { 
  Button, 
  Flex, 
  // useToast,
} from "@chakra-ui/react"
import { 
  FaFileAlt,
} from "react-icons/fa"
import { ChevronDownIcon } from '@chakra-ui/icons'
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from '@chakra-ui/react'
import { useFilePicker } from 'use-file-picker';
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { type ApiError, type FileCreate, FilesMetadataService } from "../../client"

const Navbar = () => {
  const queryClient = useQueryClient()
  // const toast = useToast()
  const mutation = useMutation({
    mutationFn: (files: File[]) => {
      const handleFileUpload = async (file: File) => {
        // send file to storage

        const metadata: FileCreate = {
          name: file.name,
          size: file.size
        };

        // send metadata to our backend
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
