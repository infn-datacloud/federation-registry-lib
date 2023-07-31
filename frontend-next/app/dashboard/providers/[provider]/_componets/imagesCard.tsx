import { Image } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, List, ListItem } from "@mui/material";
import Link from "next/link";

export default function ImagesCard({ items }: { items?: Image[] }) {
  return (
    <Card>
      <CardHeader title="Images" />
      <CardContent>
        {items ? (
          <List>
            {items.map((item, index) => (
              <Link href={`/dashboard/images/${item.uid}`}>
                <ListItem key={index} disablePadding>
                  {item.name}
                </ListItem>
              </Link>
            ))}
          </List>
        ) : (
          "No VM images"
        )}
      </CardContent>
    </Card>
  );
}
