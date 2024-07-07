import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import React from "react"
import config from "../../config"

import useCustomToast from "../../hooks/useCustomToast"
import { FilePublic, filesDeleteFile } from "../../client/axios"
import { storageDeleteFile } from "../../client/s3"

interface DeleteFileProps {
  file: FilePublic
  isOpen: boolean
  onClose: () => void
}

const Delete = ({ file, isOpen, onClose }: DeleteFileProps) => {
  const bucketName = config.REACT_APP_FILE_BUCKET_NAME;
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const cancelRef = React.useRef<HTMLButtonElement | null>(null)

  const deleteFile = async (file: FilePublic) => {
    await storageDeleteFile(bucketName, file.access_key);
    await filesDeleteFile({ fileId: file.id })
  }

  const mutation = useMutation({
    mutationFn: deleteFile,
    onSuccess: () => {
      showToast(
        "Success",
        "The file was deleted successfully.",
        "success",
      )
      onClose()
    },
    onError: () => {
      showToast(
        "An error occurred.",
        "An error occurred while deleting the file.",
        "error",
      )
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ["files"],
      })
    },
  })

  const onSubmit = async (file: FilePublic) => {
    mutation.mutate(file)
  }

  return (
    <>
      <AlertDialog
        isOpen={isOpen}
        onClose={onClose}
        leastDestructiveRef={cancelRef}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader>Delete File</AlertDialogHeader>

            <AlertDialogBody>
              Are you sure? You will not be able to undo this action.
            </AlertDialogBody>

            <AlertDialogFooter gap={3}>
              <Button 
                variant="danger" 
                type="submit" 
                onClick={() => onSubmit(file)}
              >
                Delete
              </Button>
              <Button
                ref={cancelRef}
                onClick={onClose}
              >
                Cancel
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </>
  )
}

export default Delete
