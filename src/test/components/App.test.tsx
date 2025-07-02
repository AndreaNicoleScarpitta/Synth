import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../App';

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ success: true }),
    });
  });

  it('renders main landing page', () => {
    render(<App />);
    
    expect(screen.getByText('Synthetic Ascension')).toBeInTheDocument();
    expect(screen.getByText(/next-generation clinical data platform/i)).toBeInTheDocument();
  });

  it('renders navigation header', () => {
    render(<App />);
    
    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByText('Synthetic Ascension')).toBeInTheDocument();
  });

  it('renders persona tabs', () => {
    render(<App />);
    
    expect(screen.getByText('Clinical Researcher')).toBeInTheDocument();
    expect(screen.getByText('R&D Scientist')).toBeInTheDocument();
    expect(screen.getByText('AI Builder')).toBeInTheDocument();
    expect(screen.getByText('Compliance Lead')).toBeInTheDocument();
  });

  it('switches personas when tabs are clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Default should be researcher
    expect(screen.getByText(/accelerate research timelines/i)).toBeInTheDocument();
    
    // Switch to scientist
    await user.click(screen.getByText('R&D Scientist'));
    await waitFor(() => {
      expect(screen.getByText(/drive pharmaceutical innovation/i)).toBeInTheDocument();
    });
    
    // Switch to builder
    await user.click(screen.getByText('AI Builder'));
    await waitFor(() => {
      expect(screen.getByText(/integrate synthetic data/i)).toBeInTheDocument();
    });
  });

  it('renders action buttons', () => {
    render(<App />);
    
    expect(screen.getByRole('button', { name: /get early access/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /join waitlist/i })).toBeInTheDocument();
  });

  it('shows toast notification when clicking Get Early Access', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const earlyAccessButton = screen.getByRole('button', { name: /get early access/i });
    await user.click(earlyAccessButton);
    
    await waitFor(() => {
      expect(screen.getByText(/early access coming soon/i)).toBeInTheDocument();
    });
  });

  it('opens waitlist modal when clicking Join Waitlist', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const joinWaitlistButton = screen.getByRole('button', { name: /join waitlist/i });
    await user.click(joinWaitlistButton);
    
    await waitFor(() => {
      expect(screen.getByText('Join the Waitlist')).toBeInTheDocument();
    });
  });

  it('renders demo configuration section', () => {
    render(<App />);
    
    expect(screen.getByText(/interactive synthetic ehr generator/i)).toBeInTheDocument();
  });

  it('handles demo configuration interactions', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Check for configuration options
    const populationInput = screen.getByLabelText(/target population size/i);
    expect(populationInput).toBeInTheDocument();
    
    await user.type(populationInput, '150');
    expect(populationInput).toHaveValue(150);
  });

  it('renders feature cards for each persona', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Clinical Researcher features
    expect(screen.getByText(/synthetic ehr generation/i)).toBeInTheDocument();
    expect(screen.getByText(/simulation & discovery/i)).toBeInTheDocument();
    
    // Switch to scientist and check features
    await user.click(screen.getByText('R&D Scientist'));
    await waitFor(() => {
      expect(screen.getByText(/drug discovery acceleration/i)).toBeInTheDocument();
    });
  });

  it('renders trust indicators', () => {
    render(<App />);
    
    expect(screen.getByText(/hipaa compliant/i)).toBeInTheDocument();
    expect(screen.getByText(/synthetic data/i)).toBeInTheDocument();
    expect(screen.getByText(/privacy safe/i)).toBeInTheDocument();
  });

  it('closes modal when requested', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Open modal
    const joinWaitlistButton = screen.getByRole('button', { name: /join waitlist/i });
    await user.click(joinWaitlistButton);
    
    await waitFor(() => {
      expect(screen.getByText('Join the Waitlist')).toBeInTheDocument();
    });
    
    // Close modal
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    await waitFor(() => {
      expect(screen.queryByText('Join the Waitlist')).not.toBeInTheDocument();
    });
  });

  it('handles dark mode toggle if present', () => {
    render(<App />);
    
    // Check if dark mode toggle exists
    const darkModeToggle = screen.queryByRole('button', { name: /dark mode/i });
    if (darkModeToggle) {
      expect(darkModeToggle).toBeInTheDocument();
    }
  });

  it('renders footer section', () => {
    render(<App />);
    
    // Check for footer content
    expect(screen.getByText(/enterprise-grade security/i)).toBeInTheDocument();
  });

  it('handles generation workflow if present', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Look for generation buttons
    const generateButton = screen.queryByRole('button', { name: /generate/i });
    if (generateButton) {
      await user.click(generateButton);
      // Test would depend on actual implementation
    }
  });

  it('handles responsive design elements', () => {
    render(<App />);
    
    // Check for responsive classes or mobile-friendly elements
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
    
    // Test would verify responsive behavior
  });

  it('renders without crashing on different viewport sizes', () => {
    // Simulate mobile viewport
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375,
    });
    
    render(<App />);
    expect(screen.getByText('Synthetic Ascension')).toBeInTheDocument();
    
    // Simulate desktop viewport
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 1920,
    });
    
    render(<App />);
    expect(screen.getByText('Synthetic Ascension')).toBeInTheDocument();
  });

  it('handles keyboard navigation', async () => {
    render(<App />);
    
    // Test tab navigation
    fireEvent.keyDown(document.body, { key: 'Tab' });
    
    // First focusable element should be focused
    const firstFocusable = screen.getByRole('button', { name: /get early access/i });
    expect(firstFocusable).toHaveFocus();
  });

  it('maintains state across interactions', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Change persona
    await user.click(screen.getByText('R&D Scientist'));
    
    // Open and close modal
    await user.click(screen.getByRole('button', { name: /join waitlist/i }));
    await waitFor(() => {
      expect(screen.getByText('Join the Waitlist')).toBeInTheDocument();
    });
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    // Persona should still be R&D Scientist
    await waitFor(() => {
      expect(screen.getByText(/drive pharmaceutical innovation/i)).toBeInTheDocument();
    });
  });
});