import { Card, CardContent, CardHeader, Typography } from "@mui/material";
import { Project } from "../_lib/dbTypes";

export default function ProjectCard({ item }: { item: Project }) {
  return (
    <Card>
      <CardHeader title="Project" />
      <CardContent>
        <Typography>Name: {item.name}</Typography>
        <Typography>Provider: {item.provider?.name}</Typography>
      </CardContent>
    </Card>
  );
}
