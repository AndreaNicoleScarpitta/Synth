import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WaitlistModal from '../../components/WaitlistModal';

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('WaitlistModal', () => {
  const mockOnClose = vi.fn();
  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
  };

  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ success: true }),
    });
  });

  it('renders when open', () => {
    render(<WaitlistModal {...defaultProps} />);
    
    expect(screen.getByText('Join the Waitlist')).toBeInTheDocument();
    expect(screen.getByText('Get early access to Synthetic Ascension')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(<WaitlistModal {...defaultProps} isOpen={false} />);
    
    expect(screen.queryByText('Join the Waitlist')).not.toBeInTheDocument();
  });

  it('renders all form sections', () => {
    render(<WaitlistModal {...defaultProps} />);
    
    expect(screen.getByText('Basic Information')).toBeInTheDocument();
    expect(screen.getByText('Project Details')).toBeInTheDocument();
    expect(screen.getByLabelText('Full Name *')).toBeInTheDocument();
    expect(screen.getByLabelText('Email Address *')).toBeInTheDocument();
    expect(screen.getByLabelText('Organization')).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const submitButton = screen.getByRole('button', { name: /join waitlist/i });
    await user.click(submitButton);
    
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    expect(screen.getByText('Email is required')).toBeInTheDocument();
  });

  it('validates email format', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const emailInput = screen.getByLabelText('Email *');
    await user.type(emailInput, 'invalid-email');
    
    const submitButton = screen.getByRole('button', { name: /join waitlist/i });
    await user.click(submitButton);
    
    expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    // Fill out required fields
    await user.type(screen.getByLabelText('Name *'), 'John Doe');
    await user.type(screen.getByLabelText('Email *'), 'john@example.com');
    await user.type(screen.getByLabelText('Organization'), 'Test Corp');
    
    const submitButton = screen.getByRole('button', { name: /join waitlist/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/v2/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: expect.stringContaining('"name":"John Doe"'),
      });
    });
  });

  it('shows success state after submission', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    // Fill and submit form
    await user.type(screen.getByLabelText('Name *'), 'John Doe');
    await user.type(screen.getByLabelText('Email *'), 'john@example.com');
    await user.click(screen.getByRole('button', { name: /join waitlist/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Welcome to the waitlist!')).toBeInTheDocument();
      expect(screen.getByText(/thank you for your interest/i)).toBeInTheDocument();
    });
  });

  it('handles submission errors', async () => {
    const user = userEvent.setup();
    mockFetch.mockRejectedValue(new Error('Network error'));
    
    render(<WaitlistModal {...defaultProps} />);
    
    await user.type(screen.getByLabelText('Name *'), 'John Doe');
    await user.type(screen.getByLabelText('Email *'), 'john@example.com');
    await user.click(screen.getByRole('button', { name: /join waitlist/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });

  it('closes modal when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('closes modal when backdrop is clicked', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const backdrop = screen.getByTestId('modal-backdrop');
    await user.click(backdrop);
    
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('handles escape key press', () => {
    render(<WaitlistModal {...defaultProps} />);
    
    fireEvent.keyDown(document, { key: 'Escape', code: 'Escape' });
    
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('renders help bubbles for complex fields', () => {
    render(<WaitlistModal {...defaultProps} />);
    
    // Check for help icons next to complex medical fields
    expect(screen.getByTestId('help-bubble-use-cases')).toBeInTheDocument();
    expect(screen.getByTestId('help-bubble-requirements')).toBeInTheDocument();
  });

  it('toggles design partner checkbox', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const checkbox = screen.getByLabelText(/interested in being a design partner/i);
    expect(checkbox).not.toBeChecked();
    
    await user.click(checkbox);
    expect(checkbox).toBeChecked();
  });

  it('handles company size selection', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const select = screen.getByLabelText('Company Size');
    await user.selectOptions(select, '51-200');
    
    expect(screen.getByDisplayValue('51-200')).toBeInTheDocument();
  });

  it('maintains form state during interaction', async () => {
    const user = userEvent.setup();
    render(<WaitlistModal {...defaultProps} />);
    
    const nameInput = screen.getByLabelText('Name *');
    const emailInput = screen.getByLabelText('Email *');
    
    await user.type(nameInput, 'John Doe');
    await user.type(emailInput, 'john@example.com');
    
    expect(nameInput).toHaveValue('John Doe');
    expect(emailInput).toHaveValue('john@example.com');
  });
});