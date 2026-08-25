"""
WatchSphere AI v3.0 - Invoice Generator Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from backend.models.order import Order


class InvoiceService:
    """
    Generates printable HTML invoices for orders.
    """

    @staticmethod
    def generate_invoice_html(order: Order) -> str:
        """Generates standard enterprise order HTML invoice."""
        return f"""
        <div style="padding: 30px; background: #FFFFFF; color: #0F172A; font-family: Arial, sans-serif; border-radius: 12px; border: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #6366F1; padding-bottom: 15px;">
                <div>
                    <h2 style="color: #6366F1; margin: 0;">WatchSphere AI Platform</h2>
                    <p style="margin: 4px 0; color: #64748B; font-size: 0.9rem;">Customer Insights Platform v3.0</p>
                </div>
                <div style="text-align: right;">
                    <h3 style="margin: 0;">TAX INVOICE</h3>
                    <p style="margin: 4px 0; font-weight: bold;">#{order.order_number}</p>
                    <p style="margin: 0; color: #64748B; font-size: 0.85rem;">Date: {order.order_date}</p>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; margin: 20px 0;">
                <div>
                    <strong>Billed To:</strong><br>
                    {order.customer_name}<br>
                    {order.shipping_address or 'Customer Primary Address'}
                </div>
                <div style="text-align: right;">
                    <strong>Vendor:</strong><br>
                    {order.vendor_name}<br>
                    Payment Method: {order.payment_method} ({order.payment_status})
                </div>
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <thead>
                    <tr style="background: #F1F5F9; text-align: left;">
                        <th style="padding: 10px; border: 1px solid #CBD5E1;">Item Details</th>
                        <th style="padding: 10px; border: 1px solid #CBD5E1;">Qty</th>
                        <th style="padding: 10px; border: 1px solid #CBD5E1;">Price</th>
                        <th style="padding: 10px; border: 1px solid #CBD5E1;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #E2E8F0;">Executive Timepiece Order Package</td>
                        <td style="padding: 10px; border: 1px solid #E2E8F0;">{order.items_count}</td>
                        <td style="padding: 10px; border: 1px solid #E2E8F0;">${order.total_amount:,.2f}</td>
                        <td style="padding: 10px; border: 1px solid #E2E8F0;">${order.total_amount:,.2f}</td>
                    </tr>
                </tbody>
            </table>

            <div style="text-align: right; margin-top: 20px; font-size: 1rem;">
                <p style="margin: 4px 0;">Subtotal: <strong>${order.total_amount:,.2f}</strong></p>
                <p style="margin: 4px 0;">GST ({18}%): <strong>${order.gst_amount:,.2f}</strong></p>
                <p style="margin: 4px 0; color: #6366F1; font-size: 1.3rem;">Final Amount: <strong>${order.final_amount:,.2f}</strong></p>
            </div>

            <div style="margin-top: 30px; text-align: center; font-size: 0.8rem; color: #94A3B8; border-top: 1px solid #E2E8F0; padding-top: 15px;">
                Thank you for choosing WatchSphere AI Platform. Powered by Saniya Maner | Infosys Internship Project 2026.
            </div>
        </div>
        """
