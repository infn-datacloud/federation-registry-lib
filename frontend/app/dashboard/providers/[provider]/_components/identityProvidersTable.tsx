import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { IdentityProvider } from "../../_lib/dbTypes";

export default function IdentityProvidersTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: IdentityProvider[];
}) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          <TableCell>Endpoint</TableCell>
          <TableCell>Group Claim</TableCell>
          <TableCell>Communication Name</TableCell>
          <TableCell>Communication Protocol</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items
          .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
          .map((item, index) => (
            <TableRow key={index}>
              <TableCell component="th" scope="row">
                {item.endpoint.toString()}
              </TableCell>
              <TableCell>{item.group_claim}</TableCell>
              <TableCell>{item.relationship?.idp_name}</TableCell>
              <TableCell>{item.relationship?.protocol}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
