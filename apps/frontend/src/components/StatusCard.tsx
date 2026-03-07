"use client";

import { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import { fetchHealth, type HealthResponse } from "@/lib/api";

type State =
  | { status: "loading" }
  | { status: "ok"; data: HealthResponse }
  | { status: "error"; message: string };

export function StatusCard() {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    fetchHealth()
      .then((data) => setState({ status: "ok", data }))
      .catch((err: unknown) =>
        setState({
          status: "error",
          message: err instanceof Error ? err.message : "Unknown error",
        }),
      );
  }, []);

  return (
    <Card variant="outlined" sx={{ minWidth: 340 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Backend Status
        </Typography>

        {state.status === "loading" && (
          <Box display="flex" alignItems="center" gap={1}>
            <CircularProgress size={16} />
            <Typography variant="body2" color="text.secondary">
              Connecting…
            </Typography>
          </Box>
        )}

        {state.status === "error" && (
          <Chip label={`Unreachable: ${state.message}`} color="error" size="small" />
        )}

        {state.status === "ok" && (
          <Box display="flex" flexDirection="column" gap={1}>
            <Chip label={`API ${state.data.status}`} color="success" size="small" />
            <Typography variant="caption" color="text.secondary">
              Version: {state.data.version}
            </Typography>
            {Object.entries(state.data.services).map(([name, status]) => (
              <Box key={name} display="flex" justifyContent="space-between">
                <Typography variant="body2">{name}</Typography>
                <Chip
                  label={status}
                  color={status === "ok" ? "success" : "warning"}
                  size="small"
                />
              </Box>
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
