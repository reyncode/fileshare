import { 
  Box, 
  Flex, 
  Icon, 
  Text, 
  useColorModeValue 
} from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { FiSettings } from "react-icons/fi"
import { MdOutlineCloud } from "react-icons/md";

const items = [
  { icon: MdOutlineCloud, title: "Storage", path: "/files" },
  { icon: FiSettings, title: "Settings", path: "/settings" },
]

interface SidebarItemsProps {
  onClose?: () => void
}

const SidebarItems = ({ onClose }: SidebarItemsProps) => {
  const textColor = useColorModeValue("ui.dark", "ui.light")
  const bgActive = useColorModeValue("#E2E8F0", "#4A5568")

  const listItems = items.map(({ icon, title, path }) => (
    <Flex
      as={Link}
      to={path}
      w="100%"
      p={2}
      key={title}
      activeProps={{
        style: {
          background: bgActive,
          borderRadius: "12px",
        },
      }}
      color={textColor}
      onClick={onClose}
    >
      <Icon as={icon} alignSelf="center" />
      <Text ml={2}>{title}</Text>
    </Flex>
  ))

  return (
    <>
      <Box>{listItems}</Box>
    </>
  )
}

export default SidebarItems
