import { Box } from "@chakra-ui/react"

const UserMenu = () => {

  return (
    <>
      {/* Desktop */}
      <Box
        display={{ base: "none", md: "block" }}
        position="fixed"
        top={4}
        right={4}
      >
      </Box>
    </>
  )
}

export default UserMenu
