import React, { useState } from 'react';
import Head from 'next/head';
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Stack,
  Text,
  VStack,
  HStack,
  SimpleGrid,
  Icon,
} from '@chakra-ui/react';
import { motion } from 'framer-motion';
import FeatureCard from '../components/FeatureCard';
import LeadCaptureModal from '../components/LeadCaptureModal';
import personas from '../config/personas';
import verticals from '../config/verticals';

const MotionBox = motion(Box);
const MotionStack = motion(Stack);

export default function LandingPage() {
  const [persona, setPersona] = useState('builder');
  const { headline, description, features } = personas[persona];

  return (
    <Box bg="gray.50" minH="100vh" py={20}>
      <Head>
        <title>Synthetic Ascension | Privacy-Safe Synthetic EHRs for Clinical AI</title>
        <meta
          name="description"
          content="Synthetic Ascension provides high-fidelity synthetic Electronic Health Records to accelerate clinical AI development, safe hypothesis testing, and audit-ready validation without risking patient privacy."
        />
        <meta
          name="keywords"
          content="synthetic EHRs, clinical AI, synthetic health data, AI in healthcare, rare disease simulation, agentic QA, FDA AI validation, medical data generation, privacy-safe AI, digital health"
        />
        <meta name="author" content="Synthetic Ascension" />
        <meta property="og:title" content="Synthetic Ascension | Privacy-Safe Synthetic EHRs for Clinical AI" />
        <meta
          property="og:description"
          content="Join pioneering AI teams and medical researchers using synthetic patient data to iterate faster, validate safer, and innovate earlier."
        />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://www.syntheticascension.com" />
        <meta property="og:image" content="https://www.syntheticascension.com/social-preview.png" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Synthetic Ascension | Privacy-Safe Synthetic EHRs for Clinical AI" />
        <meta
          name="twitter:description"
          content="Build and validate clinical AI tools with safe, high-quality synthetic data."
        />
        <meta name="twitter:image" content="https://www.syntheticascension.com/social-preview.png" />
      </Head>

      <Container maxW="7xl">
        {/* Hero */}
        <MotionStack
          spacing={6}
          textAlign="center"
          mb={16}
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Heading
            as="h1"
            fontSize={{ base: '3xl', md: '5xl' }}
            fontWeight="extrabold"
            bgGradient="linear(to-r, purple.600, blue.500)"
            bgClip="text"
            fontFamily="syne"
          >
            Synthetic Ascension
          </Heading>
          <Text fontSize="xl" color="gray.700" maxW="3xl" mx="auto">
            Privacy-safe synthetic EHRs to accelerate clinical AI development, model validation,
            and regulatory confidence — from day one.
          </Text>

          <HStack spacing={4} justify="center" mt={4} flexWrap="wrap">
            {Object.entries(personas).map(([key, p]) => (
              <Button
                key={key}
                onClick={() => setPersona(key)}
                colorScheme={persona === key ? 'purple' : 'gray'}
                variant={persona === key ? 'solid' : 'outline'}
              >
                {p.label}
              </Button>
            ))}
          </HStack>
        </MotionStack>

        {/* Vision Section */}
        <Stack spacing={8} mb={16} textAlign="center" px={{ base: 4, md: 0 }}>
          <Heading size="lg">Our Vision</Heading>
          <Text color="gray.700" maxW="4xl" mx="auto">
            Synthetic Ascension is building the foundation for next-generation clinical innovation.
            We generate lifelike synthetic Electronic Health Records that empower AI teams, medical
            researchers, and regulators to iterate faster, safer, and earlier — without risking real
            patient privacy.
          </Text>
          <Text color="gray.700" maxW="4xl" mx="auto">
            Our agentic QA systems continuously audit synthetic reports and datasets for plausibility,
            consistency, and completeness — ensuring every output is usable, traceable, and review-ready.
            This isn’t a replacement for real-world evidence — it’s the way to design it better.
          </Text>
        </Stack>

        {/* Persona Section */}
        <MotionBox
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <Stack spacing={8} mb={16} px={{ base: 4, md: 0 }}>
            <Heading size="lg" textAlign="center">
              {headline}
            </Heading>
            <Text textAlign="center" color="gray.600" maxW="3xl" mx="auto">
              {description}
            </Text>
            <Flex gap={10} direction={{ base: 'column', md: 'row' }} justify="center" flexWrap="wrap">
              {features.map((f, i) => (
                <FeatureCard key={i} icon={f.icon} title={f.title} desc={f.desc} />
              ))}
            </Flex>
          </Stack>
        </MotionBox>

        {/* Why Now Section */}
        <Stack spacing={8} mb={20} textAlign="center" px={{ base: 4, md: 0 }}>
          <Heading size="lg">Why Now?</Heading>
          <Text color="gray.700" maxW="4xl" mx="auto">
            AI in healthcare is outpacing access to safe and structured data. Privacy laws like HIPAA and
            GDPR are tightening. Regulators now demand explainability, fairness, and reproducibility in
            clinical AI.
          </Text>
          <Text color="gray.700" maxW="4xl" mx="auto">
            Synthetic Ascension is purpose-built for this inflection point — delivering the simulation,
            auditability, and speed required to innovate responsibly.
          </Text>
        </Stack>

        {/* Industry Verticals */}
        <Stack spacing={6} mb={20} px={{ base: 4, md: 0 }}>
          <Heading size="md" textAlign="center">
            Real Use Cases. Real Value.
          </Heading>
          <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={10}>
            {verticals.map((v, i) => (
              <FeatureCard key={i} icon={v.icon} title={v.title} desc={v.desc} />
            ))}
          </SimpleGrid>
        </Stack>

        {/* Impact Section */}
        <MotionBox
          bg="gray.100"
          p={10}
          rounded="lg"
          shadow="base"
          maxW="6xl"
          mx="auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          <Stack spacing={4} textAlign="center">
            <Heading size="md">Why This Matters</Heading>
            <Text color="gray.700" maxW="4xl" mx="auto">
              The world’s most vulnerable patients are often the least represented in data. We built
              Synthetic Ascension not just for speed or scalability — but to enable safer innovation,
              equitable research, and accessible care. No PHI. No delays. Just progress.
            </Text>
          </Stack>
        </MotionBox>

        {/* Final CTA */}
        <Stack spacing={4} mt={20} textAlign="center" px={{ base: 4, md: 0 }}>
          <Heading size="md">Join the movement.</Heading>
          <Text color="gray.600" maxW="2xl" mx="auto">
            Synthetic Ascension is already powering dozens of teams across healthcare, life sciences,
            and AI. Be part of the next wave of safer, smarter clinical innovation.
          </Text>
          <Flex justify="center">
            <LeadCaptureModal />
          </Flex>
        </Stack>
      </Container>
    </Box>
  );
}
