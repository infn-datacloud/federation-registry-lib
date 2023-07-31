import { Flavor } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, List, ListItem } from "@mui/material";
import Link from "next/link";

export default function FlavorsCard({ items }: { items?: Flavor[] }) {
  return (
    <Card>
      <CardHeader title="Flavors" />
      <CardContent>
        {items ? (
          <List>
            {items.map((item, index) => (
              <Link href={`/dashboard/flavors/${item.uid}`}>
                <ListItem key={index} disablePadding>
                  {item.name}
                </ListItem>
              </Link>
            ))}
          </List>
        ) : (
          "No VM flavors"
        )}
      </CardContent>
    </Card>
  );
}
