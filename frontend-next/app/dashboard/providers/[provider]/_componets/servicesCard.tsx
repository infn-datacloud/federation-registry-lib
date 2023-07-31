import { Service } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, List, ListItem } from "@mui/material";
import Link from "next/link";

export default function ServicesCard({ items }: { items?: Service[] }) {
  return (
    <Card>
      <CardHeader title="Services" />
      <CardContent>
        {items ? (
          <List>
            {items.map((item, index) => (
              <Link href={`/dashboard/services/${item.uid}`}>
                <ListItem key={index} disablePadding>
                  {item.endpoint.toString()}
                </ListItem>
              </Link>
            ))}
          </List>
        ) : (
          "No services available"
        )}
      </CardContent>
    </Card>
  );
}
