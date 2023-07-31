import { Project } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, List, ListItem } from "@mui/material";
import Link from "next/link";

export default function ProjectsCard({ items }: { items?: Project[] }) {
  return (
    <Card>
      <CardHeader title="Projects" />
      <CardContent>
        {items ? (
          <List>
            {items.map((item, index) => (
              <Link href={`/dashboard/projects/${item.uid}`}>
                <ListItem key={index} disablePadding>
                  {item.name}
                </ListItem>
              </Link>
            ))}
          </List>
        ) : (
          "No projects"
        )}
      </CardContent>
    </Card>
  );
}
