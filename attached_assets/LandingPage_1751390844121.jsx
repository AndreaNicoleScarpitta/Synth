import React, { useState } from 'react'
import {
  Box,
  Container,
  Heading,
  Text,
  HStack,
  Stack,
  Flex,
  SimpleGrid,
  Button as ChakraButton,
} from '@chakra-ui/react'
import { motion } from 'framer-motion'
import { FeatureCard } from '../components/ui/FeatureCard'
import { LeadCaptureModal } from '../components/ui/LeadCaptureModal'
import { Button } from '../components/ui/Button'
import personas from '../config/personas'
import verticals from '../config/verticals'

const MotionBox = motion(Box)
const MotionStack = motion(Stack)

export default function LandingPage({ onStartDemo }) {
  const [persona, setPersona] = useState('builder')
  const { headline, description, features } = personas[persona]

  return (
    <Box bg="gray.50" minH="100vh" py={20}>
      <Container maxW="7xl">
        {/* Hero */}
        <MotionStack spacing={6} textAlign="center" mb={16} initial={{ opacity: 0, y: -30 }} animate={{ opacity:1, y:0 }} transition={{ duration:0.6 }}>
          <Heading as="h1" fontSize={{ base:'3xl', md:'5xl' }} fontWeight="extrabold" bgGradient="linear(to-r, purple.600, blue.500)" bgClip="text">Synthetic Ascension</Heading>
          <Text fontSize="xl" color="gray.700" maxW="3xl" mx="auto">
            Privacy-safe synthetic EHRs to accelerate clinical AI development, model validation, and regulatory confidence — from day one.
          </Text>
          <HStack spacing={4} justify="center" mt={4} flexWrap="wrap">
            {Object.entries(personas).map(([key, p]) => (
              <ChakraButton key={key} onClick={() => setPersona(key)} colorScheme={persona===key ? 'purple':'gray'}>{p.label}</ChakraButton>
            ))}
          </HStack>
          <HStack spacing={4} justify="center" mt={4}>
            <Button variant="brandOutline" onClick={onStartDemo}>🚀 Start Demo</Button>
            <LeadCaptureModal />
          </HStack>
        </MotionStack>

        {/* rest of your Vision, Persona, Why Now, Verticals, Impact & CTA sections */}
        {/* use <FeatureCard /> inside those sections exactly as before */}
      </Container>
    </Box>
  )
}
