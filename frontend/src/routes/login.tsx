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
  Flex,
  Spacer,
  useBoolean,
  useColorMode,
} from "@chakra-ui/react"
import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router"
import { type SubmitHandler, useForm } from "react-hook-form"

import type { Body_login_login_access_token as AccessToken } from "../client/axios"
import useAuth, { isLoggedIn } from "../hooks/useAuth"
import { emailPattern } from "../utils"

export const Route = createFileRoute("/login" as never)({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/files",
      })
    }
  },
})

function Login() {
  const darkLogo = `${process.env.PUBLIC_URL}/assets/images/fileshare-logo-dark.svg`
  const lightLogo = `${process.env.PUBLIC_URL}/assets/images/fileshare-logo-light.svg`
  const { colorMode } = useColorMode()
  const [show, setShow] = useBoolean()
  const { loginMutation, error, resetError } = useAuth()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AccessToken>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  })

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    if (isSubmitting) return

    resetError()

    try {
      await loginMutation.mutateAsync(data)
    } catch {
      // error is handled by useAuth hook
    }
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
          alt="Fileshare logo"
          height="auto"
          maxW="2xs"
          alignSelf="center"
          mb={4}
        />
        <Text fontSize="md" fontWeight="semibold">Email Address</Text>
        <FormControl id="username" isInvalid={!!errors.username || !!error}>
          <Input
            id="username"
            {...register("username", {
              pattern: emailPattern,
            })}
            type="email"
            required
            variant="filled"
          />
          {errors.username && (
            <FormErrorMessage>{errors.username.message}</FormErrorMessage>
          )}
        </FormControl>

        <Flex
          alignItems="center"
        >

          <Text fontSize="md" fontWeight="semibold">Password</Text>
          <Spacer />

          <Link
            as={RouterLink} 
            to="/login" 
            color="blue.500"
            fontWeight="semibold"
          >
            Forgot password?
          </Link>

        </Flex>

        <FormControl
          id="password" 
          isInvalid={!!error}
          mb={3}
        >
          <InputGroup>
            <Input
              {...register("password")}
              type={show ? "text" : "password"}
              required
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
          Log In
        </Button>
        <Center
          gap={1}
        >
          <Text fontSize="md" >Not yet registered?</Text>
          <Link 
            as={RouterLink} 
            to="/register" 
            color="blue.500"
            fontWeight="semibold"
          >
            Create an account
          </Link>
        </Center>
      </Container>
    </>
  )
}
