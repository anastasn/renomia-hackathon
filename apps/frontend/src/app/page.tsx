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
      </Box>
    </Container>
  );
}
