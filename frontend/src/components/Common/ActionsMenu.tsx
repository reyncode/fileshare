import {
  Button,
  Menu,
  MenuButton,
  MenuDivider,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { FiDownload, FiEdit, FiTrash } from "react-icons/fi"
import { useMutation } from "@tanstack/react-query";
import { FilePublic, FilesStorageService } from "../../client"
import EditFile from "../Files/EditFile"
import Delete from "./DeleteAlert"

interface ActionsMenuProps {
  type: string
  value: FilePublic
  disabled?: boolean
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const bucketName = import.meta.env.VITE_FILE_BUCKET_URL;
  const editUserModal = useDisclosure()
  const deleteModal = useDisclosure()
  const mutation = useMutation({
    mutationFn: (file: FilePublic) => {
      return FilesStorageService.downloadFile(bucketName, file.access_key, file.name)
    },
    onSuccess: () => {
      console.log("success")
    },
    onError: (err: Error) => {
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
            onClick={editUserModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Edit {type}
          </MenuItem>
          <MenuDivider />
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>

        <EditFile
          file={value as FilePublic}
          isOpen={editUserModal.isOpen}
          onClose={editUserModal.onClose}
        />
        <Delete
          type={type}
          id={value.id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  )
}

export default ActionsMenu
