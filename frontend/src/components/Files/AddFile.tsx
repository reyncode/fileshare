import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
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

import { type ApiError, type FileCreate, FilesService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"

interface AddFileProps {
  isOpen: boolean
  onClose: () => void
}

const AddFile = ({ isOpen, onClose }: AddFileProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FileCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      path: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FileCreate) =>
      FilesService.createFile({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "File created successfully.", "success")
      reset()
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

  const onSubmit: SubmitHandler<FileCreate> = (data) => {
    mutation.mutate(data)
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
          <ModalHeader>Add File</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.path}>
              <FormLabel htmlFor="path">Path</FormLabel>
              <Input
                id="path"
                {...register("path", {
                  required: "Path is required.",
                })}
                placeholder="Path"
                type="text"
              />
              {errors.path && (
                <FormErrorMessage>{errors.path.message}</FormErrorMessage>
              )}
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default AddFile
