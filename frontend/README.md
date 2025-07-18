# Menshun Frontend

Modern React frontend for the Menshun Enterprise Privileged Access Management system, built with TypeScript, Tailwind CSS, and Azure AD integration.

## 🚀 Features

- **Modern React 18** with TypeScript and strict type checking
- **Azure AD Integration** with MSAL for authentication
- **Responsive Design** with Tailwind CSS and Solo Leveling-inspired theme
- **Component Library** with Radix UI primitives
- **State Management** with TanStack Query for server state
- **Form Handling** with React Hook Form and Zod validation
- **Testing** with Jest and React Testing Library
- **Code Quality** with ESLint, Prettier, and Husky hooks
- **Performance** optimized with Vite bundler

## 📋 Prerequisites

- Node.js 18.0.0 or higher
- npm 9.0.0 or higher
- Access to Microsoft Entra ID tenant

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your Azure AD configuration:
   ```bash
   VITE_AZURE_CLIENT_ID=your-azure-client-id
   VITE_AZURE_TENANT_ID=your-azure-tenant-id
   VITE_AZURE_REDIRECT_URI=http://localhost:3000
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   ```

## 🏃 Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Available Scripts

```bash
# Development
npm run dev              # Start development server
npm run build           # Build for production
npm run preview         # Preview production build

# Code Quality
npm run lint            # Run ESLint
npm run lint:fix        # Fix ESLint issues
npm run format          # Format code with Prettier
npm run format:check    # Check code formatting
npm run type-check      # Run TypeScript compiler

# Testing
npm run test            # Run tests
npm run test:watch      # Run tests in watch mode
npm run test:coverage   # Run tests with coverage
npm run test:ci         # Run tests for CI

# Storybook
npm run storybook       # Start Storybook dev server
npm run build-storybook # Build Storybook

# Bundle Analysis
npm run analyze         # Analyze bundle size
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components
│   └── Layout/         # Layout components
├── pages/              # Page components
│   ├── auth/           # Authentication pages
│   ├── users/          # User management pages
│   ├── service-identities/  # Service identity pages
│   ├── credentials/    # Credential management pages
│   ├── role-assignments/    # Role assignment pages
│   ├── audit/          # Audit log pages
│   └── settings/       # Settings pages
├── hooks/              # Custom React hooks
├── services/           # API service functions
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── config/             # Configuration files
├── contexts/           # React contexts
├── store/              # State management
├── assets/             # Static assets
└── styles/             # Global styles and themes
```

## 🎨 Design System

The application uses a Solo Leveling-inspired design system with:

- **Color Palette:** Dark themes with purple and gold accents
- **Typography:** Inter font family with display fonts
- **Components:** Based on Radix UI primitives
- **Animations:** Subtle animations with Framer Motion
- **Icons:** Lucide React icon library

### Theme Colors

```css
/* Primary - Shadow/Dark theme */
primary: #1e293b to #0f172a

/* Secondary - Purple for privileged actions */
secondary: #a855f7 to #7c3aed

/* Accent - Gold for highlights */
accent: #f59e0b to #d97706
```

## 🔐 Authentication

The application integrates with Microsoft Entra ID using MSAL:

```typescript
// Configuration
const msalConfig = {
  auth: {
    clientId: "your-client-id",
    authority: "https://login.microsoftonline.com/tenant-id",
    redirectUri: "http://localhost:3000"
  }
}

// Required permissions
const scopes = [
  "User.Read",
  "User.ReadWrite.All",
  "Directory.Read.All",
  "Directory.ReadWrite.All",
  "RoleManagement.Read.All",
  "RoleManagement.ReadWrite.Directory"
]
```

## 📊 State Management

- **Server State:** TanStack Query for API data fetching and caching
- **Client State:** React hooks and context for local state
- **Form State:** React Hook Form with Zod validation

Example API query:
```typescript
const { data: users, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.users.list()
})
```

## 🧪 Testing

The project uses Jest and React Testing Library:

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

Test files should be placed alongside components or in `__tests__` directories.

## 📦 Building for Production

Build the application:
```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## 🚀 Deployment

The application can be deployed to various platforms:

### Docker
```bash
# Build Docker image
docker build -t menshun-frontend .

# Run container
docker run -p 3000:3000 menshun-frontend
```

### Static Hosting
The built application is a static SPA that can be deployed to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Azure Static Web Apps

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_AZURE_CLIENT_ID` | Azure AD application client ID | Required |
| `VITE_AZURE_TENANT_ID` | Azure AD tenant ID | Required |
| `VITE_AZURE_REDIRECT_URI` | OAuth redirect URI | `http://localhost:3000` |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

### TypeScript Configuration

The project uses strict TypeScript configuration:
- Strict mode enabled
- No implicit any
- Unused locals/parameters detection
- Exact optional property types

## 🤝 Contributing

1. Follow the established code style (ESLint + Prettier)
2. Write tests for new features
3. Update documentation as needed
4. Use conventional commit messages

## 📄 License

This project is licensed under the MIT License.