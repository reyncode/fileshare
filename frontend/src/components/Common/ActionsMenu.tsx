import { useRef } from 'react';
import {
  Button,
  Menu,
  MenuButton,
  MenuDivider,
  MenuItem,
  MenuList,
  useDisclosure,
  useToast,
  ToastId,
} from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { FiDownload, FiEdit, FiTrash } from "react-icons/fi"
import { useMutation } from "@tanstack/react-query";
import RenameFile from "../Files/RenameFile"
import Delete from "../Files/DeleteFile"
import config from "../../config"
import { FilePublic } from "../../client/axios"
import { storageDownloadFile, storageOpenDownloadedBlob } from '../../client/s3';

interface ActionsMenuProps {
  value: FilePublic
  disabled?: boolean
}

const ActionsMenu = ({ value, disabled }: ActionsMenuProps) => {
  const bucketName = config.REACT_APP_FILE_BUCKET_NAME;
  const renameFileModal = useDisclosure()
  const deleteModal = useDisclosure()
  const toast = useToast()
  const toastIdRef = useRef<ToastId | undefined>(undefined);
  const mutation = useMutation<Blob | undefined, Error, FilePublic>({
    mutationFn: (file: FilePublic) => {
      toastIdRef.current = toast({
        title: `Downloading`,
        description: `File is being downloaded`,
        status: "info",
        isClosable: true,
        position: "bottom-right",
        duration: null,
      })

      return storageDownloadFile(bucketName, file.access_key)
    },
    onSuccess: (data: Blob | undefined, variables: FilePublic) => {
      if (data) {
        storageOpenDownloadedBlob(data, variables.name) 

        if (toastIdRef.current) {
          toast.update(toastIdRef.current, {
            title: "Success",
            description: "Downloaded successfully",
            status: "success",
            isClosable: true,
            position: "bottom-right",
            duration: 5000,
          })
        } else {
          console.error('Toast ID is undefined');
        }
      }
    },
    onError: (err: Error) => {
      if (toastIdRef.current) {
        toast.update(toastIdRef.current, {
          title: "Error",
          description: `${err.message}`,
          status: "error",
          isClosable: true,
          position: "bottom-right",
          duration: 5000,
        })
      } else {
        console.error('Toast ID is undefined');
      }
      console.log(err.message)
    }
  })

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          <MenuItem
            onClick={() => {mutation.mutate(value)}}
            icon={<FiDownload fontSize="16px" />}
          >
            Download
          </MenuItem>
          <MenuItem
            onClick={renameFileModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Rename
          </MenuItem>
          <MenuDivider />
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete
          </MenuItem>
        </MenuList>

        <RenameFile
          file={value as FilePublic}
          isOpen={renameFileModal.isOpen}
          onClose={renameFileModal.onClose}
        />
        <Delete
          file={value}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  )
}

export default ActionsMenu
