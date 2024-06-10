import { Button, Flex, Icon, useDisclosure } from "@chakra-ui/react"
import { 
  FaPlus, 
  FaFolder,
  FaFolderPlus,
  FaFileAlt,
} from "react-icons/fa"
import { ChevronDownIcon } from '@chakra-ui/icons'
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
} from '@chakra-ui/react'

import AddFile from "../Files/AddFile"

const Navbar = () => {
  const addFileModal = useDisclosure()

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
              icon={<FaFolderPlus />}
            >
              New Folder
            </MenuItem>
            <MenuDivider />
            <MenuItem 
              icon={<FaFileAlt />}
              onClick={addFileModal.onOpen}
            >
              File Upload
            </MenuItem>
            <MenuItem
              icon={<FaFolder />}
            >
              Folder Upload
            </MenuItem>
          </MenuList>
        </Menu>

        <AddFile isOpen={addFileModal.isOpen} onClose={addFileModal.onClose} />
      </Flex>
    </>
  )
}

export default Navbar
