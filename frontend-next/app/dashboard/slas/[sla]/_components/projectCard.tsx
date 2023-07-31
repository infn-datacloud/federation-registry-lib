import { Project } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

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
