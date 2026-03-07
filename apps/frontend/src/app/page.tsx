import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import { StatusCard } from "@/components/StatusCard";

export default function HomePage() {
  return (
    <Container maxWidth="md">
      <Box py={8} display="flex" flexDirection="column" gap={4}>
        {/* Header */}
        <Box>
          <Typography variant="h3" fontWeight={700} gutterBottom>
            Renomia Hackathon
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Monorepo starter — Next.js · FastAPI · LangGraph · ChromaDB
          </Typography>
        </Box>

        <Divider />

        {/* Live backend health check */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Services
          </Typography>
          <StatusCard />
        </Box>

        <Divider />

        {/* Quick-start guide */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Quick start
          </Typography>
          <Typography component="div" variant="body1">
            <ol>
              <li>
                Copy <code>infrastructure/env/.env.example</code> to{" "}
                <code>.env</code> at the repo root and fill in your secrets.
              </li>
              <li>
                Run <code>make dev</code> to start all services via
                docker-compose.
              </li>
              <li>
                Add your AI logic inside{" "}
                <code>packages/ai/</code> or{" "}
                <code>services/ai-engine/app/chains/</code>.
              </li>
              <li>
                Expose new REST endpoints in{" "}
                <code>services/backend/app/routers/</code> and call them from{" "}
                <code>apps/frontend/src/lib/api.ts</code>.
              </li>
            </ol>
          </Typography>
        </Box>
      </Box>
    </Container>
  );
}
