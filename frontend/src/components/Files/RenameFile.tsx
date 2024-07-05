import {
  Button,
  FormControl,
  FormErrorMessage,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import useCustomToast from "../../hooks/useCustomToast"
import { type ApiError, type FilePublic, type FileUpdate, filesUpdateFile } from "../../client/axios"

interface RenameFileProps {
  file: FilePublic
  isOpen: boolean
  onClose: () => void
}

const RenameFile = ({ file, isOpen, onClose }: RenameFileProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, errors, isDirty },
  } = useForm<FileUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: file,
  })

  const mutation = useMutation({
    mutationFn: (data: FileUpdate) =>
      filesUpdateFile({ fileId: file.id, requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "File updated successfully.", "success")
      onClose()
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail
      showToast("Something went wrong.", `${errDetail}`, "error")
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["files"] })
    },
  })

  const onSubmit: SubmitHandler<FileUpdate> = async (data) => {
    mutation.mutate(data)
  }

  const onCancel = () => {
    reset()
    onClose()
  }

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Rename</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={2}>
            <FormControl isInvalid={!!errors.name}>
              <Input
                id="name"
                {...register("name", {
                  required: "Name is required",
                })}
                type="text"
              />
              {errors.name && (
                <FormErrorMessage>{errors.name.message}</FormErrorMessage>
              )}
            </FormControl>
          </ModalBody>
          <ModalFooter gap={3}>
            <Button 
              onClick={onCancel}
              variant="outline"
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              isLoading={isSubmitting}
              isDisabled={!isDirty}
              minW={20}
            >
              Ok
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default RenameFile
