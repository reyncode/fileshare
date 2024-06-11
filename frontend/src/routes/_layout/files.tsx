import {
  Container,
  Flex,
  Heading,
  Skeleton,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { FaFolder, FaFileAlt } from "react-icons/fa"

import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { ErrorBoundary } from "react-error-boundary"
import { FilesService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"
import { datetimeFormatter } from "../../utils"

export const Route = createFileRoute("/_layout/files")({
  component: Files,
})

function FilesTableBody() {
  const { data: files } = useSuspenseQuery({
    queryKey: ["files"],
    queryFn: () => FilesService.readFiles({}),
  })

  return (
    <Tbody>
      {files.data.map((file) => (
        <Tr key={file.id}>
          <Td>{file.id}</Td>
          <Td>
            <Flex alignItems="center" gap={6}>
              {file.is_folder ? <FaFolder /> : <FaFileAlt />}
              {file.path}
            </Flex>
          </Td>
          <Td>{datetimeFormatter(file.updated_at)}</Td>
          <Td>
            <ActionsMenu type={"File"} value={file} />
          </Td>
        </Tr>
      ))}
    </Tbody>
  )
}
function FilesTable() {
  return (
    <TableContainer>
      <Table size={{ base: "sm", md: "md" }}>
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Path</Th>
            <Th>Last Modified</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <ErrorBoundary
          fallbackRender={({ error }) => (
            <Tbody>
              <Tr>
                <Td colSpan={4}>Something went wrong: {error.message}</Td>
              </Tr>
            </Tbody>
          )}
        >
          <Suspense
            fallback={
              <Tbody>
                {new Array(5).fill(null).map((_, index) => (
                  <Tr key={index}>
                    {new Array(4).fill(null).map((_, index) => (
                      <Td key={index}>
                        <Flex>
                          <Skeleton height="20px" width="20px" />
                        </Flex>
                      </Td>
                    ))}
                  </Tr>
                ))}
              </Tbody>
            }
          >
            <FilesTableBody />
          </Suspense>
        </ErrorBoundary>
      </Table>
    </TableContainer>
  )
}

function Files() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        My Files
      </Heading>

      <Navbar />
      <FilesTable />
    </Container>
  )
}