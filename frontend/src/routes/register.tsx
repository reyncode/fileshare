import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons"
import {
  Button,
  Center,
  Container,
  FormControl,
  FormErrorMessage,
  Icon,
  Image,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  useBoolean,
  useColorMode,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import {
  Link as RouterLink,
  createFileRoute,
  useNavigate,
} from "@tanstack/react-router"
import { type SubmitHandler, useForm } from "react-hook-form"

import { emailPattern } from "../utils"
import { useState } from "react"
import { AxiosError } from "axios"
import { type ApiError, UserCreate, usersRegisterUser } from "../client/axios"

export const Route = createFileRoute("/register" as never)({
  component: Register
})

interface UserCreateForm extends UserCreate {
  confirm_password: string
}

function Register () {
  const darkLogo = `${process.env.PUBLIC_URL}/assets/images/fileshare-logo-dark.svg`
  const lightLogo = `${process.env.PUBLIC_URL}/assets/images/fileshare-logo-light.svg`
  const { colorMode } = useColorMode()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()
  const [show, setShow] = useBoolean()
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors, isSubmitting },
  } = useForm<UserCreateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      email: "",
      password: "",
      confirm_password: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: UserCreate) =>
      usersRegisterUser({ requestBody: data }),
    onSuccess: () => {
      reset()
      navigate({ to: "/login" })
    },
    onError: (err: ApiError) => {
      let errDetail = (err.body as any)?.detail

      if (err instanceof AxiosError) {
        errDetail = err.message
      }

      if (Array.isArray(errDetail)) {
        errDetail = "Something went wrong"
      }

      setError(errDetail)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
    },
  })

  const onSubmit: SubmitHandler<UserCreateForm> = (data) => {
    mutation.mutate(data)
  }

  return (
    <>
      <Container
        as="form"
        onSubmit={handleSubmit(onSubmit)}
        h="100vh"
        maxW="sm"
        alignItems="stretch"
        justifyContent="center"
        gap={4}
        centerContent
      >
        <Image
          src={ colorMode === "light" ? darkLogo : lightLogo }
          alt="FastAPI logo"
          height="auto"
          maxW="2xs"
          alignSelf="center"
          mb={4}
        />
        <Text fontSize="md" fontWeight="semibold">Email Address</Text>
        <FormControl 
          isRequired 
          isInvalid={!!errors.email || !!error}
        >
          <Input
            id="email"
            {...register("email", {
              required: "Email is required",
              pattern: emailPattern,
            })}
            type="email"
            variant="filled"
          />
          {errors.email && (
            <FormErrorMessage>{errors.email.message}</FormErrorMessage>
          )}
        </FormControl>
        <Text fontSize="md" fontWeight="semibold">Password</Text>
        <FormControl 
          isRequired 
          isInvalid={!!errors.password || !!error}
        >
          <InputGroup>
            <Input
              id="password"
              {...register("password", {
                required: "Password is required",
                minLength: {
                  value: 8,
                  message: "Password must be at least 8 characters",
                },
              })}
              type={show ? "text" : "password"}
              variant="filled"
            />
            <InputRightElement
              color="ui.dim"
              _hover={{
                cursor: "pointer",
              }}
            >
              <Icon
                onClick={setShow.toggle}
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <ViewOffIcon /> : <ViewIcon />}
              </Icon>
            </InputRightElement>
          </InputGroup>

          {errors.password && (
            <FormErrorMessage>{errors.password.message}</FormErrorMessage>
          )}
          {errors.confirm_password && (
            <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>
          )}

        </FormControl>
        <Text fontSize="md" fontWeight="semibold">Confirm Password</Text>
        <FormControl
          isRequired
          isInvalid={!!errors.confirm_password || !!error}
          mb={3}
        >
          <InputGroup>
            <Input
              id="confirm_password"
              {...register("confirm_password", {
                required: "Please confirm your password",
                validate: (value) =>
                  value === getValues().password ||
                  "The passwords do not match",
              })}
              type={show ? "text" : "password"}
              variant="filled"
            />
            <InputRightElement
              color="ui.dim"
              _hover={{
                cursor: "pointer",
              }}
            >
              <Icon
                onClick={setShow.toggle}
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <ViewOffIcon /> : <ViewIcon />}
              </Icon>
            </InputRightElement>
          </InputGroup>
          {error && <FormErrorMessage>{error}</FormErrorMessage>}
        </FormControl>
        <Button
          variant="primary" 
          type="submit" 
          isLoading={isSubmitting}
        >
          Create account
        </Button>
        <Center
          gap={1}
        >
          <Text fontSize="md" >Already have an account?</Text>
          <Link 
            as={RouterLink} 
            to="/login" 
            color="blue.500"
            fontWeight="semibold"
          >
            Sign in 
          </Link>
        </Center>
      </Container>
    </>
  )
}
