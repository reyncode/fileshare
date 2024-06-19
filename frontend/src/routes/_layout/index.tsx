import { Container } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/" as never)({
  component: Dashboard,
})

function Dashboard() {

  return (
    <>
      <Container maxW="full">
      </Container>
    </>
  )
}
