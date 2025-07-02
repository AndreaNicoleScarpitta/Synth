import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import HelpBubble from '../../components/HelpBubble';

describe('HelpBubble', () => {
  const defaultProps = {
    content: 'This is help content',
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders trigger icon', () => {
    render(<HelpBubble {...defaultProps} />);
    
    const helpIcon = screen.getByRole('button');
    expect(helpIcon).toBeInTheDocument();
  });

  it('shows content on hover by default', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} />);
    
    const helpIcon = screen.getByRole('button');
    await user.hover(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('This is help content')).toBeInTheDocument();
    });
  });

  it('hides content on mouse leave with hover trigger', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} />);
    
    const helpIcon = screen.getByRole('button');
    await user.hover(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('This is help content')).toBeInTheDocument();
    });
    
    await user.unhover(helpIcon);
    
    await waitFor(() => {
      expect(screen.queryByText('This is help content')).not.toBeInTheDocument();
    });
  });

  it('shows content on click with click trigger', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('This is help content')).toBeInTheDocument();
    });
  });

  it('toggles content on repeated clicks', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    
    // First click - show
    await user.click(helpIcon);
    await waitFor(() => {
      expect(screen.getByText('This is help content')).toBeInTheDocument();
    });
    
    // Second click - hide
    await user.click(helpIcon);
    await waitFor(() => {
      expect(screen.queryByText('This is help content')).not.toBeInTheDocument();
    });
  });

  it('renders title when provided', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} title="Help Title" trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('Help Title')).toBeInTheDocument();
    });
  });

  it('renders close button with click trigger', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      const closeButton = screen.getByRole('button', { name: /close/i });
      expect(closeButton).toBeInTheDocument();
    });
  });

  it('closes content when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('This is help content')).toBeInTheDocument();
    });
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    await waitFor(() => {
      expect(screen.queryByText('This is help content')).not.toBeInTheDocument();
    });
  });

  it('handles complex content object', async () => {
    const user = userEvent.setup();
    const complexContent = {
      description: 'Complex help description',
      examples: ['Example 1', 'Example 2'],
    };
    
    render(<HelpBubble content={complexContent} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('Complex help description')).toBeInTheDocument();
      expect(screen.getByText('Examples:')).toBeInTheDocument();
      expect(screen.getByText('Example 1')).toBeInTheDocument();
      expect(screen.getByText('Example 2')).toBeInTheDocument();
    });
  });

  it('handles examples prop', async () => {
    const user = userEvent.setup();
    render(
      <HelpBubble 
        {...defaultProps} 
        examples={['Prop Example 1', 'Prop Example 2']} 
        trigger="click" 
      />
    );
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('Examples:')).toBeInTheDocument();
      expect(screen.getByText('Prop Example 1')).toBeInTheDocument();
      expect(screen.getByText('Prop Example 2')).toBeInTheDocument();
    });
  });

  it('renders different sizes correctly', () => {
    const { rerender } = render(<HelpBubble {...defaultProps} size="sm" />);
    expect(screen.getByRole('button')).toBeInTheDocument();
    
    rerender(<HelpBubble {...defaultProps} size="md" />);
    expect(screen.getByRole('button')).toBeInTheDocument();
    
    rerender(<HelpBubble {...defaultProps} size="lg" />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('positions bubble correctly', async () => {
    const user = userEvent.setup();
    const positions = ['top', 'bottom', 'left', 'right'] as const;
    
    for (const position of positions) {
      const { rerender } = render(
        <HelpBubble {...defaultProps} position={position} trigger="click" />
      );
      
      const helpIcon = screen.getByRole('button');
      await user.click(helpIcon);
      
      await waitFor(() => {
        expect(screen.getByText('This is help content')).toBeInTheDocument();
      });
      
      // Clean up for next iteration
      await user.click(helpIcon);
      rerender(<div />);
    }
  });

  it('handles null content gracefully', () => {
    render(<HelpBubble content={null as any} />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles undefined examples gracefully', async () => {
    const user = userEvent.setup();
    const contentWithUndefinedExamples = {
      description: 'Content without examples',
      examples: undefined,
    };
    
    render(<HelpBubble content={contentWithUndefinedExamples} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      expect(screen.getByText('Content without examples')).toBeInTheDocument();
      expect(screen.queryByText('Examples:')).not.toBeInTheDocument();
    });
  });

  it('applies correct CSS classes and styles', async () => {
    const user = userEvent.setup();
    render(<HelpBubble {...defaultProps} trigger="click" />);
    
    const helpIcon = screen.getByRole('button');
    await user.click(helpIcon);
    
    await waitFor(() => {
      const bubble = screen.getByText('This is help content').closest('div');
      expect(bubble).toHaveStyle({
        position: 'absolute',
        zIndex: '1000',
      });
    });
  });
});